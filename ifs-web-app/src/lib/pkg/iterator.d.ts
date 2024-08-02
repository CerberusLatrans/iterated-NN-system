/* tslint:disable */
/* eslint-disable */
/**
* A single affine transformation in 3D space
*/
export class AffineTransformation {
  free(): void;
/**
* Create a new affine transformation from matrix components
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
*/
  static init(): void;
/**
* Create a new IFS with the given transformations
* @param {(AffineTransformation)[]} transformations
* @returns {IteratedFunctionSystem}
*/
  static new(transformations: (AffineTransformation)[]): IteratedFunctionSystem;
/**
* @param {(AffineTransformation)[]} transformations
* @param {Float32Array} probabilities
* @returns {IteratedFunctionSystem}
*/
  static new_from_probabilities(transformations: (AffineTransformation)[], probabilities: Float32Array): IteratedFunctionSystem;
/**
* @param {(AffineTransformation)[]} transformations
* @param {MarkovChain} chain
* @returns {IteratedFunctionSystem}
*/
  static new_from_markov(transformations: (AffineTransformation)[], chain: MarkovChain): IteratedFunctionSystem;
/**
* Generate points using the IFS
* @param {number} num_points
* @returns {PtrTuple}
*/
  generate_colors(num_points: number): PtrTuple;
/**
* Generate points using the IFS
* @param {number} num_points
* @returns {number}
*/
  generate(num_points: number): number;
}
/**
*/
export class MarkovChain {
  free(): void;
/**
* @param {Float32Array} flat_matrix
* @param {number} n
* @returns {MarkovChain}
*/
  static new(flat_matrix: Float32Array, n: number): MarkovChain;
/**
* @param {Float32Array} probabilities
* @returns {MarkovChain}
*/
  static from_probabilities(probabilities: Float32Array): MarkovChain;
}
/**
* Pointer Tuple class (to export to JS frontend)
*/
export class PtrTuple {
  free(): void;
/**
*/
  color_map: number;
/**
*/
  colors_ptr: number;
/**
*/
  points_ptr: number;
}
