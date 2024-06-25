<script lang='ts'>
    import { transformations } from './stores';
    import MatrixEditor from './MatrixEditor.svelte'

    function addTransformation() {
        let id_transform = new Float32Array([
            1,0,0,0,
            0,1,0,0,
            0,0,1,0
        ])
        let new_id = Math.max(Math.max(...Array.from($transformations.keys()))+1, 0)
        $transformations.set(new_id, id_transform)
        console.log($transformations.size)
        $transformations = $transformations
    }

    function deleteTransformation(id: number) {
        if ($transformations.size > 1) {
            $transformations.delete(id)
            $transformations = $transformations
        }
    }

    function noise(id:number, a=0.05, b=0.05) {
        let aff = $transformations.get(id)!
        let noise = new Float32Array(
            [randn(a), randn(a), randn(a), randn(a),
            randn(a), randn(a), randn(a), randn(b),
            randn(a), randn(a), randn(a), randn(b)]
        )
        let noisy_aff = aff.map((n,i) => n+noise[i])
        $transformations.set(id, noisy_aff)
        $transformations = $transformations
    }
    function randn(n = 1) {
        let sign = Math.random() < 0.5 ? -1 : 1
        let val = sign*Math.random()*n
        return val
    }
</script>

<div
style:width="50%">
    <button on:click={() => {addTransformation()}}>
        Add Transformation
    </button>
    {#each $transformations as [id, matrix] (id)}
        <p>Transformation {id}</p>
        <MatrixEditor bind:matrix={matrix}></MatrixEditor>
        <button on:click={() => {noise(id)}}>
            Noise
        </button>
        <button on:click={() => {deleteTransformation(id)}}>
            Delete
        </button>
        <div
        style:color="black"
        style:height="1px"
        style:width="100%"
        style:margin="5px"
        style:border="5px"></div>
    {/each}
</div>

