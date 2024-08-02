<script lang='ts'>
    import {memory} from "../../lib/pkg/iterator_bg.wasm";
    import * as THREE from 'three';
    import { T } from '@threlte/core'
    import { Align, OrbitControls, interactivity } from '@threlte/extras'
    import { locks } from "../stores";

    const F = 5;
    const Z = -F;
    export let matrix;
    export let id;

    $: color = $locks.has(id) ? 'black' : 'red';
    const points = new Float32Array([
        Z,Z,Z, F,Z,Z, Z,F,Z, Z,Z,F,
        F,F,Z, F,Z,F, Z,F,F, F,F,F
    ])
    const id_vertices = new THREE.BufferGeometry().setAttribute(
        'position', new THREE.BufferAttribute(points.slice(0), 3))

    $: vertices = new THREE.BufferGeometry().setAttribute(
        'position', new THREE.BufferAttribute(points.slice(0), 3))
        .applyMatrix4(matrix);

    const edges = new Float32Array([
        Z,Z,Z, F,Z,Z,
        Z,Z,Z, Z,F,Z,
        Z,Z,Z, Z,Z,F,

        F,Z,Z, F,F,Z,
        F,Z,Z, F,Z,F,

        Z,F,Z, F,F,Z,
        Z,F,Z, Z,F,F,

        Z,Z,F, F,Z,F,
        Z,Z,F, Z,F,F,

        F,F,F, Z,F,F,
        F,F,F, F,Z,F,
        F,F,F, F,F,Z
    ]);
    $: edgesGeometry = new THREE.BufferGeometry().setAttribute(
        'position', new THREE.BufferAttribute(edges.slice(0), 3)).applyMatrix4(matrix);

    $: material = new THREE.LineBasicMaterial( {
        color: color,
        linewidth: 100*F,
        linecap: 'round', //ignored by WebGLRenderer
        linejoin:  'round' //ignored by WebGLRenderer
    } );
    $: segments = new THREE.LineSegments(edgesGeometry, material);


    let id_material = new THREE.LineBasicMaterial( {
        color: 'black',
        linewidth: 100*F,
        linecap: 'round', //ignored by WebGLRenderer
        linejoin:  'round' //ignored by WebGLRenderer
    } );
    const id_segments = new THREE.LineSegments(
        new THREE.BufferGeometry().setAttribute(
        'position',
        new THREE.BufferAttribute(edges.slice(0), 3)
        ), id_material);
</script>

<T.Mesh>
    <T is={segments}/>
    <T.MeshBasicMaterial color={color}/>
</T.Mesh>
<T.Points>
    <T is={vertices} />
    <T.PointsMaterial size={F/4} color={color}/>
</T.Points>

<T.Mesh>
    <T is={id_segments}/>
    <T.MeshBasicMaterial color='black'/>
</T.Mesh>
<T.Points>
    <T is={id_vertices} />
    <T.PointsMaterial size={F/2} color='black'/>
</T.Points>
