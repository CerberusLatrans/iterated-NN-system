<script lang='ts'>
    import {AffineTransformation, IteratedFunctionSystem, MarkovChain} from "../lib/pkg/iterator";
    import { Canvas } from '@threlte/core';
    import { transformations } from './stores';
    import SplitPane from './SplitPane.svelte';
    import Scene from './Scene.svelte';
    import ControlPanel from './AffinePanel.svelte';
    import { PtrTuple } from "$lib/pkg/iterator_bg";
    
    const n = 100_000
    IteratedFunctionSystem.init();

    let mkv = MarkovChain.from_probabilities(new Float32Array([0.01, 0.1, 0.1, 0.7]));
    let mkv2 = MarkovChain.new(new Float32Array([0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7, 0.01, 0.1, 0.1, 0.7]), 4)

    //$: affineTransforms = Array.from($transformations.values()).map((t) => AffineTransformation.new(t))
    //$: affineTransforms, console.log(affineTransforms)
    //$: ifs = IteratedFunctionSystem.new(affineTransforms);
    //$: ifs = IteratedFunctionSystem.new_from_probabilities(affineTransforms, new Float32Array([0.01, 0.1, 0.1, 0.7]))
    //$: ifs, console.log("IFS", ifs)

    //$: ifs2 = IteratedFunctionSystem.new_from_markov(affineTransforms, mkv)
    //$: ifs2, console.log("IFS2", ifs2)

    //$: pointsPtr = ifs.generate(n);
    //$: pointsPtr, console.log(pointsPtr)
    
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
        </svelte:fragment>
        <svelte:fragment slot="right">
            <ControlPanel></ControlPanel>
        </svelte:fragment>
    </SplitPane>
</main>

