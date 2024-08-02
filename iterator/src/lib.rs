use nalgebra::{Matrix4, Vector4};
use rand::distributions::{WeightedIndex, Uniform};
use rand::prelude::ThreadRng;
use rand::Rng;
use wasm_bindgen::prelude::*;
use hsv::hsv_to_rgb;
use web_sys::js_sys::Array;

extern crate console_error_panic_hook;
extern crate web_sys;

// A macro to provide `println!(..)`-style syntax for `console.log` logging.
macro_rules! log {
    ( $( $t:tt )* ) => {
        web_sys::console::log_1(&format!( $( $t )* ).into());
    }
}

type Point = (f32, f32, f32);

#[wasm_bindgen]
pub struct MarkovChain {
    chain: Vec<WeightedIndex<f32>>,
    rng: ThreadRng,
    idx: usize,
}

#[wasm_bindgen]
impl MarkovChain {
    pub fn new(flat_matrix: Vec<f32>, n: usize) -> MarkovChain {
        let mut matrix: Vec<Vec<f32>> = Vec::new();
        for i in 0..n {
            let row = flat_matrix[n*i..n*(i+1)].to_vec();
            matrix.push(row);
        }
        let mut rng = rand::thread_rng();
        let uni = Uniform::new(0, matrix.len());
        let idx = rng.sample(uni);

        let chain = matrix.iter().map(
            |dist| WeightedIndex::new(dist).unwrap()).collect();

        Self {
            chain,
            rng,
            idx,
        }
    }
    pub fn from_probabilities(probabilities: Vec<f32>) -> MarkovChain {
        //Self::new((0..probabilities.len()).into_iter().map(|_| probabilities.clone()).collect())
        Self::new(
            (0..probabilities.len().pow(2)).into_iter()
                .map(|i| probabilities[i%probabilities.len()]).collect(),
            probabilities.len())
    }
}

impl Iterator for MarkovChain {
    type Item = usize;
    fn next(&mut self) -> Option<Self::Item> {
        let dist = &self.chain[self.idx];
        let new_idx = self.rng.sample(&dist);
        self.idx = new_idx;
        Some(new_idx)
    }
}

/// A single affine transformation in 3D space
#[derive(Debug, Clone, Copy)]
#[wasm_bindgen]
pub struct AffineTransformation {
    matrix: Matrix4<f32>,
}

#[wasm_bindgen]
impl AffineTransformation {
    /// Create a new affine transformation from matrix components
    pub fn new(x: Vec<f32>) -> Self {
        AffineTransformation {
            matrix: Matrix4::new(x[0], x[1], x[2], x[3],
                                 x[4], x[5], x[6], x[7],
                                 x[8], x[9], x[10], x[11],
                                 0.0, 0.0, 0.0, 1.0),
        }
    }

    /// Compute the determinant
    fn determinant(&self) -> f32 {
        let determinant = self.matrix.fixed_view::<3, 3>(0, 0).determinant().abs();
        determinant
    }

    /// Apply the affine transformation to a point (x, y, z)
    fn apply(&self, point: Vector4<f32>) -> Vector4<f32> {
        self.matrix * point
    }
}

/// Pointer Tuple class (to export to JS frontend)
#[wasm_bindgen]
pub struct PtrTuple {
    pub points_ptr: *const Point,
    pub colors_ptr: *const Point,
    pub color_map: *const Point,
}

/// The Iterated Function System class
#[wasm_bindgen]
pub struct IteratedFunctionSystem {
    transformations: Vec<AffineTransformation>,
    chain: MarkovChain,
}

#[wasm_bindgen]
impl IteratedFunctionSystem {
    pub fn init() {
        console_error_panic_hook::set_once();
    }

    /// Create a new IFS with the given transformations
    pub fn new(transformations: Vec<AffineTransformation>) -> Self {
        let probabilities = transformations.iter()
            .map(|trans| trans.determinant())
            .collect::<Vec<_>>();

        // Normalize probabilities
        let total: f32 = probabilities.iter().sum();
        let probabilities = probabilities.into_iter().map(|p| p / total).collect();
        Self::new_from_probabilities(transformations, probabilities)
    }

    pub fn new_from_probabilities(transformations: Vec<AffineTransformation>, probabilities: Vec<f32>) -> Self {
        let chain = MarkovChain::from_probabilities(probabilities);
        Self::new_from_markov(transformations, chain)
    }

    pub fn new_from_markov(transformations: Vec<AffineTransformation>, chain: MarkovChain) -> Self {
        Self {
            transformations,
            chain,
        }
    }

    /// Generate points using the IFS
    pub fn generate_colors(&mut self, num_points: usize) -> PtrTuple {
        let mut points = Vec::with_capacity(num_points);
        let mut point = Vector4::new(0.0, 0.0, 0.0, 1.0);
        let mut colors = Vec::with_capacity(num_points);
        let color_map: Vec<Point> = (0..self.transformations.len()).map(|i| {
            let color = hsv_to_rgb(360.0 * i as f64/self.transformations.len() as f64, 1.0, 1.0);
            (color.0 as f32 / 255.0, color.1 as f32 / 255.0, color.2 as f32 / 255.0)
        }).collect();

        for _ in 0..num_points {
            colors.push(color_map[self.chain.idx]);
            let index = self.chain.next().unwrap();
            let transformation = &self.transformations[index];
            point = transformation.apply(point);
            points.push((point.x, point.y, point.z));
        }

        PtrTuple {points_ptr: points.as_ptr(), colors_ptr: colors.as_ptr(), color_map: color_map.as_ptr()}
        //points.as_ptr()
    }

    /// Generate points using the IFS
    pub fn generate(&mut self, num_points: usize) -> *const Point {
        let mut points = Vec::with_capacity(num_points);
        let mut point = Vector4::new(0.0, 0.0, 0.0, 1.0);

        for _ in 0..num_points {
            let index = self.chain.next().unwrap();
            let transformation = &self.transformations[index];
            point = transformation.apply(point);
            points.push((point.x, point.y, point.z));
        }

        points.as_ptr()
    }
}