<script lang='ts'>
    import {AffineTransformation, IteratedFunctionSystem} from "../lib/pkg/iterator";
    import { Canvas } from '@threlte/core';
    import { transformations } from './stores';
    import SplitPane from './SplitPane.svelte';
    import Scene from './Scene.svelte';
    import ControlPanel from './AffinePanel.svelte';
    
    const n = 100_000
    $: affineTransforms = Array.from($transformations.values()).map((t) => AffineTransformation.new(t))
    $: ifs = IteratedFunctionSystem.new(affineTransforms);
    $: pointsPtr = ifs.generate(n);
</script>

<main>
    <SplitPane>
        <svelte:fragment slot="left">
            <Canvas size={{width:500,height:700}}>
                <Scene {pointsPtr} {n}/>
            </Canvas>
        </svelte:fragment>
        <svelte:fragment slot="right">
            <ControlPanel></ControlPanel>
        </svelte:fragment>
    </SplitPane>
</main>

