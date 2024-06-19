<script>
    import {AffineTransformation, IteratedFunctionSystem} from "$lib/pkg/iterator";
    import {memory} from "$lib/pkg/iterator_bg.wasm";
    import * as THREE from 'three';
    import { T } from '@threlte/core'
    import { Align, OrbitControls, interactivity } from '@threlte/extras'


    console.log('scene')
    let a1 = AffineTransformation.new(...[0, 0, 0, 0,
                                    0, 0.16, 0, 0,
                                    0, 0, 0.16, 0])
    let a2 = AffineTransformation.new(...[0.85, 0.04, 0.04, 0,
                                        -0.04, 0.85, 0.04, 1.6,
                                        -0.04, -0.04, 0.85, 0])
    let a3 = AffineTransformation.new(...[0.20, -0.26, -0.26, 0,
                                        0.23, 0.22, -0.26, 1.6,
                                        0.23, 0.23, 0.24, 0])   
    let a4 = AffineTransformation.new(...[-0.15, 0.28, 0.28, 0,
                                            0.26, 0.24, 0.28, -5,
                                            0.26, 0.26, 0.39, 0])  
    let ifs = IteratedFunctionSystem.new([a1, a2, a3, a4]);
    let n = 1_000_000;
    let pointsPtr = ifs.generate(n);
    let points = new Float32Array(memory.buffer, pointsPtr, n*3);
    const pointCloud = new THREE.BufferGeometry();
    pointCloud.setAttribute('position', new THREE.BufferAttribute(points, 3));

    interactivity()
</script>


<T.PerspectiveCamera
  makeDefault
  position={[50, 50, 50]}
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
</Align>
