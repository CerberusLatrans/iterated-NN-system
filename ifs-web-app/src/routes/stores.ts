import {AffineTransformation, IteratedFunctionSystem} from "../lib/pkg/iterator";
import type { Float } from "@threlte/extras";
import {writable} from 'svelte/store';
import { onMount } from 'svelte';

const a1mat: Float32Array = new Float32Array([0.16, 0, 0, 0,
    0, 0.3, -0.75, 0,
    0, 0, 0.16, 0.5])
const a2mat = new Float32Array([0.85, 0.04, 0.04, 0,
    -0.04, 0.8, 0.03, 1,
    -0.04, -0.05, 0.85, 0])
const a3mat = new Float32Array([0.20, -0.2, -0.4, 0,
    0.23, 0.22, -0.26, 1.6,
    0.23, 0.23, 0.24, 0])
const a4mat = new Float32Array([-0.15, 0.28, 0.28, 0,
    -0.75, 0.24, 0.28, 0.45,
    0.26, 0.26, 0.39, 0])

let initial_transformations = new Map<number, Float32Array>();
initial_transformations.set(0, a1mat);
initial_transformations.set(1, a2mat);
initial_transformations.set(2, a3mat);
initial_transformations.set(3, a4mat);

export const transformations = writable(initial_transformations);

let initial_locks = new Map<number, Set<number>>();
initial_locks.set(0, new Set());
initial_locks.set(1, new Set());
initial_locks.set(2, new Set());
initial_locks.set(3, new Set());
export const subLocks = writable(initial_locks);
export const locks = writable(new Set());

export const showRotation = writable(true);
export const showColors = writable(false);
export const showTransforms = writable(true);