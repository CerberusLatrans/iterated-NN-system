use nalgebra::{Matrix4, Vector4};
use rand::distributions::{Distribution, WeightedIndex};//, Uniform};
//use rand::prelude::ThreadRng;
//use rand::Rng;
use wasm_bindgen::prelude::*;

type Point = (f64, f64, f64);

///#[wasm_bindgen]
///pub struct MarkovChain {
///    chain: Vec<WeightedIndex<f64>>,
///    rng: ThreadRng,
///    idx: usize,
///}
///
///#[wasm_bindgen]
///impl MarkovChain {
///    pub fn new(matrix: Vec<Vec<f64>>) -> MarkovChain {
///        let mut rng = rand::thread_rng();
///        let uni = Uniform::new(0, matrix.len());
///        let idx = rng.sample(uni);
///
///        let chain = matrix.iter().map(
///            |dist| WeightedIndex::new(dist).unwrap()).collect();
///        MarkovChain {
///            chain,
///            rng,
///            idx,
///        }
///    }
///    pub fn from_probabilities(probabilities: Vec<f64>) -> MarkovChain {
///        Self::new((0..probabilities.len()).into_iter().map(|_| probabilities.clone()).collect())
///    }
///}

///impl Iterator for MarkovChain {
///    type Item = usize;
///    fn next(&mut self) -> Option<Self::Item> {
///        let dist = &self.chain[self.idx];
///        let new_idx = self.rng.sample(&dist);
///        self.idx = new_idx;
///        Some(new_idx)
///    }
///}

/// A single affine transformation in 3D space
#[derive(Debug, Clone, Copy)]
#[wasm_bindgen]
pub struct AffineTransformation {
    matrix: Matrix4<f64>,
}

#[wasm_bindgen]
impl AffineTransformation {
    /// Create a new affine transformation from matrix components
    pub fn new(a: f64, b: f64, c: f64, d: f64,
           e: f64, f: f64, g: f64, h: f64,
           i: f64, j: f64, k: f64, l: f64) -> Self {
        AffineTransformation {
            matrix: Matrix4::new(a, b, c, d,
                                 e, f, g, h,
                                 i, j, k, l,
                                 0.0, 0.0, 0.0, 1.0),
        }
    }

    /// Compute the determinant
    fn determinant(&self) -> f64 {
        let determinant = self.matrix.fixed_view::<3, 3>(0, 0).determinant().abs();
        determinant
    }

    /// Apply the affine transformation to a point (x, y, z)
    fn apply(&self, point: Vector4<f64>) -> Vector4<f64> {
        self.matrix * point
    }
}

/// The Iterated Function System class
#[wasm_bindgen]
pub struct IteratedFunctionSystem {
    transformations: Vec<AffineTransformation>,
    probabilities: Vec<f64>,
}

#[wasm_bindgen]
impl IteratedFunctionSystem {

    /// Create a new IFS with the given transformations
    pub fn new(transformations: Vec<AffineTransformation>) -> Self {
        let probabilities = transformations.iter()
            .map(|trans| trans.determinant())
            .collect::<Vec<_>>();

        // Normalize probabilities
        let total: f64 = probabilities.iter().sum();
        let probabilities = probabilities.into_iter().map(|p| p / total).collect();

        IteratedFunctionSystem {
            transformations,
            probabilities,
        }
    }

    /// Generate points using the IFS
    pub fn generate(&self, num_points: usize) -> *const Point {
        let mut rng = rand::thread_rng();
        let dist = WeightedIndex::new(&self.probabilities).unwrap();
        
        let mut points = Vec::with_capacity(num_points);
        let mut point = Vector4::new(0.0, 0.0, 0.0, 1.0);

        for _ in 0..num_points {
            let index = dist.sample(&mut rng);
            let transformation = &self.transformations[index];
            point = transformation.apply(point);
            points.push((point.x, point.y, point.z));
        }

        points.as_ptr()
    }
}

/**
pub fn voxelize(points: Vec<(f64, f64, f64)>, size: usize) -> Vec<(isize, isize, isize)>{
p_min = points.min(axis=0)
p_max = points.max(axis=0)
return (points-p_min)/(p_max-p_min)
rescaled = normalized*np.asarray(dim)
coordinates = np.floor(rescaled).astype(int)
np.array([[x, height-y] for x,y in coords])
points
}

#[wasm_bindgen]
pub fn iterate(ifs: IteratedFunctionSystem, n: usize)
-> *const (isize, isize, isize) {
  // Generate points using the IFS
  let points = ifs.generate(n);
  let voxels = voxelize(points, n);
  voxels.as_ptr()
}
*/
pub struct Foo {}