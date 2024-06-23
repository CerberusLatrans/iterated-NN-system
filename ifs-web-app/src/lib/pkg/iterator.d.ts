/* tslint:disable */
/* eslint-disable */
/**
*#[wasm_bindgen]
*pub struct MarkovChain {
*    chain: Vec<WeightedIndex<f32>>,
*    rng: ThreadRng,
*    idx: usize,
*}
*
*#[wasm_bindgen]
*impl MarkovChain {
*    pub fn new(matrix: Vec<Vec<f32>>) -> MarkovChain {
*        let mut rng = rand::thread_rng();
*        let uni = Uniform::new(0, matrix.len());
*        let idx = rng.sample(uni);
*
*        let chain = matrix.iter().map(
*            |dist| WeightedIndex::new(dist).unwrap()).collect();
*        MarkovChain {
*            chain,
*            rng,
*            idx,
*        }
*    }
*    pub fn from_probabilities(probabilities: Vec<f32>) -> MarkovChain {
*        Self::new((0..probabilities.len()).into_iter().map(|_| probabilities.clone()).collect())
*    }
*}
*impl Iterator for MarkovChain {
*    type Item = usize;
*    fn next(&mut self) -> Option<Self::Item> {
*        let dist = &self.chain[self.idx];
*        let new_idx = self.rng.sample(&dist);
*        self.idx = new_idx;
*        Some(new_idx)
*    }
*}
* A single affine transformation in 3D space
*/
export class AffineTransformation {
  free(): void;
/**
* Create a new affine transformation from matrix components
*pub fn new(a: f32, b: f32, c: f32, d: f32,
*       e: f32, f: f32, g: f32, h: f32,
*       i: f32, j: f32, k: f32, l: f32) -> Self {
*    AffineTransformation {
*        matrix: Matrix4::new(a, b, c, d,
*                             e, f, g, h,
*                             i, j, k, l,
*                             0.0, 0.0, 0.0, 1.0),
*    }
*}
* @param {Float32Array} x
* @returns {AffineTransformation}
*/
  static new(x: Float32Array): AffineTransformation;
}
/**
* The Iterated Function System class
*/
export class IteratedFunctionSystem {
  free(): void;
/**
* Create a new IFS with the given transformations
* @param {(AffineTransformation)[]} transformations
* @returns {IteratedFunctionSystem}
*/
  static new(transformations: (AffineTransformation)[]): IteratedFunctionSystem;
/**
* Generate points using the IFS
* @param {number} num_points
* @returns {number}
*/
  generate(num_points: number): number;
}
