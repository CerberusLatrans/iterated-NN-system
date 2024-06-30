<script lang='ts'>
    import { label } from "three/examples/jsm/nodes/Nodes.js";

    export let matrix: Float32Array;
    const valueNames = [
        "Scl X", "XY-Shr X", "XZ-Shr X", "Trlt X",
        "XY-Shr Y", "Scl Y", "YZ-Shr Y", "Trlt Y",
        "XZ-Shr Z", "YZ-Shr Z", "Scl Z", "Trlt Z"]

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
        <div>
            {valueNames[i]}
            <input type="number"
            bind:value={value}
            min="-{range(i)}"
            max="{range(i)}"
            step=0.05/>
            <input type="range"
            bind:value={value}
            min="-{range(i)}"
            max="{range(i)}"
            step=0.05/>
        </div>
    {/each}
</div>