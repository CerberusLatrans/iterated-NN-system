<script lang='ts'>
    export let matrix: Float32Array;

</script>

<div 
style:display="grid"
style:grid-template-columns="repeat(4, 1fr)"
style:grid-template-rows="repeat(3, 1fr)">
    {#each matrix as value}
        <div>
            <input type="number" bind:value={value} min="-1" max="1" step=0.1/>
            <input type="range" bind:value={value} min="-1" max="1" step=0.1/>
        </div>
    {/each}
</div>