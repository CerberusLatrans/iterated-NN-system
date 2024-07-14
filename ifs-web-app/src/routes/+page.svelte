<script lang='ts'>
    import {AffineTransformation, IteratedFunctionSystem, MarkovChain} from "../lib/pkg/iterator";
    import { Canvas } from '@threlte/core';
    import { transformations, showRotation, showColors, showTransforms } from './stores';
    import SplitPane from './components/SplitPane.svelte';
    import Scene from './components/Scene.svelte';
    import ControlPanel from './components/AffinePanel.svelte';
    import { runInference, ifsFromArray } from "./inference";
    import { bool, rotate } from "three/examples/jsm/nodes/Nodes.js";
    
    const n = 100_000
    IteratedFunctionSystem.init();

    //let mkv = MarkovChain.from_probabilities(new Float32Array([0.01, 0.1, 0.1, 0.7]));
    //let mkv2 = MarkovChain.new(new Float32Array([0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7]), 4)

    const inferIFS = async (e: Event) => {
        let text = (e.target as HTMLInputElement).value
        let prediction: Float32Array = await runInference(text);
        $transformations = ifsFromArray(prediction);
    }

    function generate(ifs, n) {
        if ($showColors) {
            return ifs.generate_colors(n)
        } else {
            let pointsPtr = ifs.generate(n)
            return {
                points_ptr: pointsPtr,
                colors_ptr: null,
            }
        }
    }
    
    
    $: ptrTuple = generate(IteratedFunctionSystem.new(
    Array.from($transformations.values())
    .map((t) => AffineTransformation.new(t))), n);
</script>

<main>
    <SplitPane>
        <svelte:fragment slot="left">
            <label>
                <input type="checkbox" bind:checked={$showTransforms}>
                Show IFS Affine Transforms
            </label>
            <label>
                <input type="checkbox" bind:checked={$showColors}>
                Show IFS Colors (can cause freezing)
            </label>
            <label>
                <input type="checkbox" bind:checked={$showRotation}>
                Rotate
            </label>
            <Canvas size={{width:500,height:700}}>
                <Scene pointsPtr={ptrTuple.points_ptr} colorsPtr={ptrTuple.colors_ptr} {n}/>
            </Canvas>
            <input
            style:width='80%'
            style:height='5%'
            type="text" on:input={inferIFS} placeholder="Enter Your Prompt"/>
        </svelte:fragment>
        <svelte:fragment slot="right">
            <ControlPanel></ControlPanel>
        </svelte:fragment>
    </SplitPane>
</main>

