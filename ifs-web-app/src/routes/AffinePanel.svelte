<script lang='ts'>
    import { transformations } from './stores';
    import MatrixEditor from './MatrixEditor.svelte'
    import { read } from '$app/server';

    function addTransformation() {
        let id_transform = new Float32Array([
            1,0,0,0,
            0,1,0,0,
            0,0,1,0
        ])
        let new_id = Math.max(Math.max(...Array.from($transformations.keys()))+1, 0)
        $transformations.set(new_id, id_transform)
        $transformations = $transformations
    }

    let downloadName = 'unnamedIFS.json'

    function saveIFS(name: string) {
        const jsonString = JSON.stringify(Object.fromEntries($transformations))
        const blob = new Blob([jsonString], {type: 'application/json'});
        const blobURL = URL.createObjectURL(blob)
        const a = document.createElement('a');
        a.href = blobURL;
        a.download = name;
        a.style.display = 'none';
        document.body.append(a);
        a.click();
        setTimeout(() => {
            URL.revokeObjectURL(blobURL);
            a.remove();
        }, 1000);
    }

    function importIFS(e: Event) {
        function parseJSON(json: JSON) {
            let importedIFS = new Map()
            const jsonMap = new Map(Object.entries(json))
            jsonMap.forEach(
                (value: JSON, key) => {
                    let affine = new Map(Object.entries(value)).values()
                    importedIFS.set(parseInt(key), new Float32Array([...affine]))
                }
            )
            $transformations = importedIFS
        }
        let file = (e.target as HTMLInputElement).files![0]
        new Response(file).json().then(parseJSON)
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

    function determinant(matrix: Float32Array) {
        let [a,b,c,d,e,f,g,h,i] =[
        matrix[0], matrix[1], matrix[2],
        matrix[4], matrix[5], matrix[6],
        matrix[8], matrix[9], matrix[10]]
        return a*e*i + b*f*g + c*d*h - c*e*g - b*d*i - a*f*h
    }

    function randomIFS() {
        $transformations.forEach((v, k) => {
            let a = [-0.75, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.75]
            let b = [-1.5, -1.25, -1, -0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1, 1.25, 1.5]
            let randomAffine = new Float32Array([
                choose(a),choose(a),choose(a),choose(b),
                choose(a),choose(a),choose(a),choose(b),
                choose(a),choose(a),choose(a),choose(b)
            ])
            $transformations.set(k, randomAffine)
            $transformations = $transformations
        })
    }

    function choose(choices: number[]) {
        var index = Math.floor(Math.random() * choices.length);
        return choices[index];
    }
</script>

<div
style:width="50%">
    <button on:click={() => {addTransformation()}}>Add Transformation</button>
    <button on:click={() => {randomIFS()}}>Randomize</button>
    <button on:click={() => {saveIFS(downloadName)}}>Download</button>
    <input bind:value={downloadName} />
    <input accept="application/json" type="file" on:change={importIFS}/>
    {#each $transformations as [id, matrix] (id)}
        <p>Transformation {id} (det={determinant(matrix).toFixed(2)})</p>
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

