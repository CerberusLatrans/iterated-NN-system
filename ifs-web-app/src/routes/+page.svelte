<script lang='ts'>
    import {AffineTransformation, IteratedFunctionSystem} from "../lib/pkg/iterator";
    import { Canvas } from '@threlte/core';
    import { transformations } from './stores';
    import SplitPane from './SplitPane.svelte';
    import Scene from './Scene.svelte';
    import ControlPanel from './AffinePanel.svelte';
    
    $: affineTransforms = Array.from($transformations.values()).map((t) => AffineTransformation.new(t))
    $: ifs = IteratedFunctionSystem.new(affineTransforms);
</script>


<main>
    <SplitPane>
        <svelte:fragment slot="left">
            <Canvas size={{width:500,height:700}}>
                <Scene {ifs}/>
            </Canvas>
        </svelte:fragment>
        <svelte:fragment slot="right">
            <ControlPanel></ControlPanel>
        </svelte:fragment>
    </SplitPane>
</main>

