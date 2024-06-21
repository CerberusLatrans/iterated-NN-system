<script lang='ts'>
    import {memory} from "$lib/pkg/iterator_bg.wasm";
    import * as THREE from 'three';
    import { T } from '@threlte/core'
    import { Align, OrbitControls, interactivity } from '@threlte/extras'

    export let a,b,c,d,e,f,g,h,i,j,k,l;
    const matrix = new THREE.Matrix4();
    matrix.set(a,b,c,d,e,f,g,h,i,j,k,l, 0, 0, 0, 1)

    let corners = new Float32Array([
        0,0,0,
        0,0,1,
        0,1,0,
        0,1,1,
        1,0,0,
        1,0,1,
        1,1,0,
        1,1,1,
    ]);
    let vertices = new THREE.BufferGeometry()
    vertices.setAttribute('position', new THREE.BufferAttribute(corners, 3));
    vertices.applyMatrix4(matrix)
    console.log(vertices)
    let segments = new THREE.LineSegments(vertices);
    console.log(segments)
</script>

<T.Mesh>
    <T is={segments}/>
    <T.MeshBasicMaterial color="red" />
</T.Mesh>
