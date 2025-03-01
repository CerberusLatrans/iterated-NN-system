<script lang='ts'>
    import { label } from "three/examples/jsm/nodes/Nodes.js";
    import { subLocks } from "../stores";
    import { get } from "svelte/store";

    export let id: number;
    export let matrix: Float32Array;
    const valueNames = [
        "Scl X", "Shr XY", "Shr XZ", "Trlt X",
        "Shr YX", "Scl Y", "Shr YZ", "Trlt Y",
        "Shr ZX", "Shr ZY", "Scl Z", "Trlt Z"]

    function range(idx: number) {
        if ((idx+1)%4 == 0) {
            return 2
        } else {
            return 1
        }
    }

</script>

<div 
style:display="grid"
style:grid-template-columns="repeat(4, 1fr)"
style:grid-template-rows="repeat(3, 1fr)">
    {#each matrix as value, i}
        <div
        style:display="grid"
        style:grid-template=
        "'label label value value' 1em 'lock slider slider slider' 1em / 1em 4em 2em 2em">
            <input type="checkbox" id="lock" style:grid-area="lock" on:change={
            ()=>$subLocks.get(id)?.has(i) ? $subLocks.get(id)?.delete(i) : $subLocks.get(id)?.add(i)}>
            <div style:grid-area="label">{valueNames[i]}</div>
            <input type="number"
            bind:value={value}
            style:grid-area="value"
            min="-{range(i)}"
            max="{range(i)}"
            step=0.05/>
            <input type="range"
            bind:value={value}
            style:grid-area="slider"
            min="-{range(i)*2}"
            max="{range(i)*2}"
            step=0.05/>
        </div>
    {/each}
</div>