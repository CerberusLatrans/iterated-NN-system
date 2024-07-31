<script lang='ts'>
    import {AffineTransformation, IteratedFunctionSystem, MarkovChain} from "../lib/pkg/iterator";
    import { Canvas } from '@threlte/core';
    import { transformations, showRotation, showColors, showTransforms } from './stores';
    import SplitPane from './components/SplitPane.svelte';
    import Scene from './components/Scene.svelte';
    import ControlPanel from './components/AffinePanel.svelte';
    import { runInference, ifsFromArray } from "./inference";
    import { bool, rotate, timerDelta } from "three/examples/jsm/nodes/Nodes.js";
    import { ifsInterpolate } from "./ifsUtils";
    import { onMount } from "svelte";
    
    let n = 100_000
    IteratedFunctionSystem.init();
    let prompt = "Barnsley leafy fern";
    const delay = (ms) => new Promise(res => setTimeout(res, ms));
    //let mkv = MarkovChain.from_probabilities(new Float32Array([0.01, 0.1, 0.1, 0.7]));
    //let mkv2 = MarkovChain.new(new Float32Array([0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7]), 4)
    async function inferIFS() {
        let text = prompt;
        let prediction: Float32Array = await runInference(text);
        let ifsInterpolation = ifsInterpolate($transformations,ifsFromArray(prediction), undefined,50,0,1);
        for (let i=0; i<ifsInterpolation.length; i++) {
            if (i>0) {await delay(50);}
            $transformations = ifsInterpolation[i];
        }    
    };

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
                Show IFS Colors (may freeze)
            </label>
            <label>
                <input type="checkbox" bind:checked={$showRotation}>
                Rotate
            </label>
            <label>
                <input type="range" min="{100}" max="{100_000}" bind:value={n}>
                <input type="number"
                    bind:value={n}
                    min="-{100}"
                    max="{100000}"
                    step=1/>
                points
            </label>
            <Canvas size={{width:500,height:700}}>
                <Scene pointsPtr={ptrTuple.points_ptr} colorsPtr={ptrTuple.colors_ptr} {n}/>
            </Canvas>
            {#await inferIFS()}
                <p>loading model...</p>
            {:then x}
                <p>model loaded</p>
            {/await}
            <input
            style:width='80%'
            style:height='5%'
            type="search" bind:value={prompt} placeholder="Enter Your Prompt"/>
            <button on:click={inferIFS}>Submit</button>
        </svelte:fragment>
        <svelte:fragment slot="right">
            <ControlPanel></ControlPanel>
        </svelte:fragment>
    </SplitPane>
</main>

