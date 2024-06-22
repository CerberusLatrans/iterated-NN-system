<script lang='ts'>
    import { transformations } from './stores';
    import MatrixEditor from './MatrixEditor.svelte'
</script>

<div
style:width="50%">
    {#each $transformations as [id, matrix]}
        <MatrixEditor bind:matrix={matrix}></MatrixEditor>
    {/each}
</div>

