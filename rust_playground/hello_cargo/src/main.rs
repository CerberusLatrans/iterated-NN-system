use nalgebra::{Matrix4, Vector4};
use rand::distributions::{Distribution, WeightedIndex};

/// A single affine transformation in 3D space
#[derive(Debug, Clone, Copy)]
struct AffineTransformation {
    matrix: Matrix4<f64>,
}

impl AffineTransformation {
    /// Create a new affine transformation from matrix components
    fn new(a: f64, b: f64, c: f64, d: f64,
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
struct IteratedFunctionSystem {
    transformations: Vec<AffineTransformation>,
    probabilities: Vec<f64>,
}

impl IteratedFunctionSystem {

    /// Create a new IFS with the given transformations
    fn new(transformations: Vec<AffineTransformation>) -> Self {
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
    fn generate(&self, num_points: usize) -> Vec<(f64, f64, f64)> {
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

        points
    }
}

fn main() {
    // Example usage of the IFS class

    // Define some affine transformations in 3D
    let transformations = vec![
        AffineTransformation::new(0.5, 0.0, 0.0, 0.0,
                                  0.0, 0.5, 0.0, 0.0,
                                  0.0, 0.0, 0.5, 0.0),
        AffineTransformation::new(0.5, 0.0, 0.0, 0.5,
                                  0.0, 0.5, 0.0, 0.0,
                                  0.0, 0.0, 0.5, 0.0),
        AffineTransformation::new(0.5, 0.0, 0.0, 0.25,
                                  0.0, 0.5, 0.0, 0.5,
                                  0.0, 0.0, 0.5, 0.5),
    ];


    // Create the IFS
    let ifs = IteratedFunctionSystem::new(transformations);

    // Generate points using the IFS
    let points = ifs.generate(10000);

    // Print the generated points
    for point in points {
        println!("{}, {}, {}", point.0, point.1, point.2);
    }
}