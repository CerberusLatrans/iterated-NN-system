<script lang='ts'>
    import { transformations } from './stores';
    import MatrixEditor from './MatrixEditor.svelte'
</script>

<div
style:width="50%">
    {#each $transformations as [id, matrix]}
        <MatrixEditor bind:matrix={matrix}></MatrixEditor>
        <div
        style:color="black"
        style:height="5px"
        style:width="100%"
        style:margin="20px"
        style:border="5px"></div>
    {/each}
</div>

