<script lang='ts'>
    import {AffineTransformation, IteratedFunctionSystem} from "$lib/pkg/iterator";
    import { Canvas } from '@threlte/core';
    import { transformations } from './stores';
    import SplitPane from './SplitPane.svelte';
    import Scene from './Scene.svelte';
    import ControlPanel from './ControlPanel.svelte';
    
    $: affineTransforms = Array.from($transformations.values()).map((t) => AffineTransformation.new(t))
    $: ifs = IteratedFunctionSystem.new(affineTransforms);
    let randor = 0;

    function randomize(n = 4) {
        let new_transforms = new Map();
        for (let step = 0; step < n; step++) {
            new_transforms.set(n, random_affine(0.7, 1));
        }
        new_transforms.set(0, $transformations.get(0))
        new_transforms.set(1, $transformations.get(1))
        //new_transforms.set(2, $transformations.get(2))
        new_transforms.set(3, $transformations.get(3))
        $transformations = new_transforms
    }
    function random_affine(a = 1, b = 1) {
        return new Float32Array(
            [randn(a), randn(a), 0, 0,
            0, randn(a), randn(a), randn(b),
            randn(a), randn(a), 0, randn(b)]
        )
    }
    function randn(n = 1) {
        let sign = Math.random() < 0.5 ? 1 : 1
        let val = sign*Math.random()*n
        return val
    }
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<main>
    <SplitPane>
        <svelte:fragment slot="left">
            <button on:click={() => {randomize()}}>
                {`Randomize`}
            </button>
            <Canvas size={{width:500,height:700}}>
                <Scene {ifs} numba={randor}/>
            </Canvas>
        </svelte:fragment>
        <svelte:fragment slot="right">
            <ControlPanel></ControlPanel>
        </svelte:fragment>
    </SplitPane>
</main>

