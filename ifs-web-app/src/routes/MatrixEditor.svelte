<script lang='ts'>
    export let matrix: Float32Array;

</script>

<div 
style:display="grid"
style:grid-template-columns="repeat(4, 1fr)">
    {#each matrix as value}
        <input type="number" bind:value={value} min="-2" max="2" step=0.1/>
        <input type="range" bind:value={value} min="-2" max="2" step=0.1/>
    {/each}
</div>