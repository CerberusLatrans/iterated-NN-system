<script>
	import Counter from './Counter.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
    import {AffineTransformation, IteratedFunctionSystem} from "$lib/pkg/iterator";
    import { Canvas } from '@threlte/core';
    import Scene from './Scene.svelte';
    import { transformations } from './stores';

    $: transforms = [...$transformations.values()]
    $: ifs = IteratedFunctionSystem.new(transforms);
    let randor = 0;

    function randomize(n = 4) {
        let new_transforms = new Map();
        for (let step = 0; step < n; step++) {
            new_transforms.set(n, random_affine(0.75, -0.5));
        }
        ///let new_transforms = new Map();
        ///new_transforms.set(0, $transformations.get(0))
        ///new_transforms.set(1, $transformations.get(1))
        ///new_transforms.set(3, $transformations.get(3))
        ///new_transforms.set(2, random_affine(1, 1));
        $transformations = new_transforms
        console.log("Changed");
    }
    function random_affine(a = 1, b = 1) {
        return AffineTransformation.new(
            randn(a), randn(a), randn(a), randn(b),
            randn(a), randn(a), randn(a), randn(b),
            randn(a), randn(a), randn(a), randn(b)
        )
    }
    function randn(n = 1) {
        let sign = Math.random() < 0.5 ? 1 : 1
        let val = sign*Math.random()*n
        console.log(val)
        return val
    }
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<button on:click={() => {randomize()}}>
	{`Randomize`}
</button>
<Canvas size={{width:1000,height:750}}>
    <Scene {ifs} numba={randor}/>
</Canvas>
