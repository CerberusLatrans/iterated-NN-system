import {AffineTransformation, IteratedFunctionSystem} from "$lib/pkg/iterator";
import type { Float } from "@threlte/extras";
import {writable} from 'svelte/store';

const a1mat: Float32Array = new Float32Array([0.16, 0, 0, 0,
    0, 0.16, 0, 0,
    0, 0, 0.16, 0])
const a2mat = new Float32Array([0.85, 0.04, 0.04, 0,
    -0.04, 0.8, 0.03, 1,
    -0.04, -0.05, 0.85, 0])
const a3mat = new Float32Array([0.20, -0.2, -0.4, 0,
    0.23, 0.22, -0.26, 1.6,
    0.23, 0.23, 0.24, 0])
const a4mat = new Float32Array([-0.15, 0.28, 0.28, 0,
    0.2, 0.24, 0.28, 0.45,
    0.26, 0.26, 0.39, 0])
//let a1 = AffineTransformation.new(a1mat);
//let a2 = AffineTransformation.new(...)
//let a3 = AffineTransformation.new(...)   
//let a4 = AffineTransformation.new(...)  

//let transformations = $state([a1, a2, a3, a4])
//let ifs: IteratedFunctionSystem = $derived(IteratedFunctionSystem.new(transformations))
//let randor: number = $state(0);
let initial_transformations = new Map<number, Float32Array>();
initial_transformations.set(0, a1mat);
initial_transformations.set(1, a2mat);
initial_transformations.set(2, a3mat);
initial_transformations.set(3, a4mat);
//initial_transformations.set(4, a4mat);

export const transformations = writable(initial_transformations);