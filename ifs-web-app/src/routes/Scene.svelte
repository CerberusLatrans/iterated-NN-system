<script>
    import {memory} from "$lib/pkg/iterator_bg.wasm";
    import * as THREE from 'three';
    import { T } from '@threlte/core'
    import { Align, OrbitControls, interactivity } from '@threlte/extras'
    import Affine from './Affine.svelte';
    import Counter from "./Counter.svelte";
    
    ///let {ifs: IteratedFunctionSystem, numba} = $props()
    ///let n = 1_000_000;
    ///let pointsPtr = $derived(ifs.generate(n));
    ///let points = $derived(new Float32Array(memory.buffer, pointsPtr, n*3));
    
    export let ifs;
    export let numba;

    let n = 100_000;
    $: pointsPtr = ifs.generate(n);
    $: points = new Float32Array(memory.buffer, pointsPtr, n*3);

    $: pointCloud = new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(points, 3));

    let size = 10
    let divisions = 5
    const yGrid = new THREE.GridHelper(size, divisions)
    const xGrid = new THREE.GridHelper(size, divisions)
    const zGrid = new THREE.GridHelper(size, divisions)
    xGrid.rotation.x = Math.PI/2
    zGrid.rotation.z = Math.PI/2
    interactivity()

    const a1Mat = {a:1, b:1, c:1, d:0,
        e:0, f:1, g:0, h:0,
        i:0, j:0, k:1, l:0}
    console.log('Scene', numba);
</script>


<T.PerspectiveCamera
  makeDefault
  position={[25, 25, 25]}
  fov={15}
>
<OrbitControls/>
</T.PerspectiveCamera>
<T.DirectionalLight
  position.y={10}
  position.z={10}
/>

<Align>
    <T.Points>
      <T is={pointCloud} />
      <T.PointsMaterial size={0.25} color='black'/>
    </T.Points>
    <T is={xGrid} />
    <T is={yGrid} />
    <T is={zGrid} />
    <Affine  {...a1Mat}/>
</Align>
