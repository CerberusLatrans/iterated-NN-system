<script lang='ts'>
    import {AffineTransformation, IteratedFunctionSystem, MarkovChain} from "../lib/pkg/iterator";
    import { Canvas } from '@threlte/core';
    import { transformations } from './stores';
    import SplitPane from './components/SplitPane.svelte';
    import Scene from './components/Scene.svelte';
    import ControlPanel from './components/AffinePanel.svelte';
    import { runInference } from "./inference";
    
    const n = 10_000
    IteratedFunctionSystem.init();

    //let mkv = MarkovChain.from_probabilities(new Float32Array([0.01, 0.1, 0.1, 0.7]));
    //let mkv2 = MarkovChain.new(new Float32Array([0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7]), 4)

    const inferIFS = async (e: Event) => {
        let text = (e.target as HTMLInputElement).value
        let prediction = await runInference(text);
        //$transformations = toMap(prediction);
    }
    
    $: ptrTuple = IteratedFunctionSystem.new(
        Array.from($transformations.values())
        .map((t) => AffineTransformation.new(t))).generate(n);
</script>

<main>
    <SplitPane>
        <svelte:fragment slot="left">
            <Canvas size={{width:500,height:700}}>
                <Scene pointsPtr={ptrTuple.points_ptr} colorsPtr={ptrTuple.colors_ptr} {n}/>
            </Canvas>
            <input type="text" on:input={inferIFS}/>
        </svelte:fragment>
        <svelte:fragment slot="right">
            <ControlPanel></ControlPanel>
        </svelte:fragment>
    </SplitPane>
</main>

