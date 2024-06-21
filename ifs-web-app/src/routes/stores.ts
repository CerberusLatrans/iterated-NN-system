import {AffineTransformation, IteratedFunctionSystem} from "$lib/pkg/iterator.js";
import {writable} from 'svelte/store';


let a1 = AffineTransformation.new(...[0.16, 0, 0, 1,
    0, 0.16, 0, 0,
    0, 0, 0.16, 0]);
let a2 = AffineTransformation.new(...[0.85, 0.04, 0.04, 0,
                           -0.04, 0.8, 0.03, -1,
                           -0.04, -0.05, 0.85, 0])
let a3 = AffineTransformation.new(...[0.20, -0.2, -0.4, 0,
                           0.23, 0.22, -0.26, 1.6,
                           0.23, 0.23, 0.24, 0])   
let a4 = AffineTransformation.new(...[-0.15, 0.28, 0.28, 0,
                               0.2, 0.24, 0.28, 0.45,
                               0.26, 0.26, 0.39, 0])  
let a5 = AffineTransformation.new(...[0.5, 0, 0, 0,
                                -1, 0, 1, 0,
                                1, 0, 0.5, 0])  
//let transformations = $state([a1, a2, a3, a4])
//let ifs: IteratedFunctionSystem = $derived(IteratedFunctionSystem.new(transformations))
//let randor: number = $state(0);
let initial_transformations = new Map<number, AffineTransformation>();
initial_transformations.set(0, a1);
initial_transformations.set(1, a2);
initial_transformations.set(2, a3);
initial_transformations.set(3, a4);
initial_transformations.set(4, a5);

export const transformations = writable(initial_transformations);