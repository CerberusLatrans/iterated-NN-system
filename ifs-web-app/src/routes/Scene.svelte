<script>
    import {memory} from "../lib/pkg/iterator_bg.wasm";
    import * as THREE from 'three';
    import { T } from '@threlte/core'
    import { Align, OrbitControls, interactivity } from '@threlte/extras'
    import {AffineTransformation, IteratedFunctionSystem} from "../lib/pkg/iterator";
    import AffineVisual from './AffineVisual.svelte';
    import { transformations } from './stores';
    
    export let ifs;

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
    
    <!--
    <T is={xGrid} />
    <T is={yGrid} />
    <T is={zGrid} />
    -->
    
    {#each $transformations as [id, m]}
        <AffineVisual matrix={
            new THREE.Matrix4(
            m[0], m[1], m[2], m[3],
            m[4], m[5], m[6], m[7],
            m[8], m[9], m[10], m[11],
            0, 0, 0, 1)
        }></AffineVisual>
    {/each}
</Align>
