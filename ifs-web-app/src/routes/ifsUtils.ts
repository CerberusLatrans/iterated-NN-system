function closestMapping(
    a: Map<number, Float32Array>,
    b: Map<number, Float32Array>
): Map<number, number> {
    let closest_dist: number = Number.POSITIVE_INFINITY;
    let closest_perm_map: Map<number, number> = new Map();
    
    let a_keys = Array.from(a.keys())
    let b_keys = Array.from(b.keys())
    let perms = permutations(b_keys.length)
    for (var perm_idx=0; perm_idx<perms.length; perm_idx++) {
        let perm = perms[perm_idx];
        let total_dist = 0;
        let new_perm_map = new Map();
        for (var i=0; i<perm.length; i++) {
            let a_key = a_keys[i];
            let b_key = b_keys[perm[i]];
            total_dist += affineDist(a.get(a_key)!, b.get(b_key)!);
            new_perm_map.set(a_key, b_key);
        }
        if (total_dist<closest_dist) {
            closest_dist = total_dist;
            closest_perm_map = new_perm_map;
        }
    }
    return closest_perm_map;
}

function affineDist(a: Float32Array, b:Float32Array): number {
    let dist = 0;
    for (var i = 0; i < a.length; i++) {
        dist += Math.abs(a[i] - b[i]);
    }
    return dist;
}

function permutations(n: number): Array<Array<number>> {
    let results: Array<Array<number>> = [];
  
    function permute(arr: Array<number>, memo: Array<number> = []) {
        var cur, memo = memo || [];

        for (var i = 0; i < arr.length; i++) {
            cur = arr.splice(i, 1);
            if (arr.length === 0) {
                results.push(memo.concat(cur));
            }
            permute(arr.slice(), memo.concat(cur));
            arr.splice(i, 0, cur[0]);
        }
            return results;
    }
   
   let range = [];
   for (let i=0; i<n; i++) {
    range.push(i);
   }
   return permute(range);
  }

function affineInterpolate(
    a: Float32Array,
    b: Float32Array,
    steps: number = 10,
    start: number = 0,
    end: number = 1,
): Array<Float32Array> {
    let stepSize = (end-start)/(steps-1)
    let affineSeries = [];
    for (let t=0; t<steps; t++) {
        let bWeight = start+(t*stepSize);
        let aWeight = 1-bWeight;
        affineSeries.push(affineMean([a,b], [aWeight,bWeight]));
    }
    return affineSeries
}

function affineMean(affines: Array<Float32Array>, weights: Array<number> = []): Float32Array {
    let avgArray = new Float32Array(affines[0].length);
    let equalWeights = [];
    for (let i=0; i<affines.length; i++) {
        equalWeights.push(1/affines.length)
    }
    weights = weights ? weights : equalWeights
    for (let i=0; i<affines[0].length; i++) {
        let avgElement = 0
        for (let j=0; j<affines.length; j++) {
            avgElement += weights[j]*affines[j][i]
        }
        avgArray[i] = avgElement;
    }
    return avgArray;
}

export function ifsInterpolate(
    a: Map<number, Float32Array>,
    b: Map<number, Float32Array>,
    mapping: Map<number, number> = closestMapping(a, b),
    steps: number = 10,
    start: number = 1,
    end: number = 1,
): Array<Map<number, Float32Array>> {
    let ifsSeries = []; // shape: (steps, arity)
    let arity = a.size;
    let affineMapping = Array.from(mapping.entries());
    
    let interpolationSet: Float32Array[][] = [] // shape: (arity, steps)
    for (let i=0; i<arity; i++) {
        let aAffine = a.get(affineMapping[i][0])!;
        let bAffine = b.get(affineMapping[i][1])!;
        let affineSeries = affineInterpolate(aAffine, bAffine, steps, start, end);
        interpolationSet.push(affineSeries);
    } 

    for (let t=0; t<steps; t++) {
        let ifs = new Map();
        for (let i=0; i<arity; i++) {
            ifs.set(i, interpolationSet[i][t])
        }
        ifsSeries.push(ifs)
    }
    return ifsSeries
}

export function scaleObject(ifs: Map<number, Float32Array>, factor: number) {
    let scaledIfs = new Map();
    ifs.forEach((v, k) => {
        v[3] = v[3]*factor
        v[7] = v[7]*factor
        v[11] = v[11]*factor
        scaledIfs.set(k, v);
    });
    return scaledIfs;
}

export function rotateObject(
    ifs: Map<number, Float32Array>,
    rad: number,
    about: string
): Map<number, Float32Array> {
    ifs.forEach((v, k) => {
        let rotatedAffineA = rotateAffineA(v, rad, about);
        let rotatedAffineB = rotateAffineB(v, rad, about);
        rotatedAffineA[3] = rotatedAffineB[3];
        rotatedAffineA[7] = rotatedAffineB[7];
        rotatedAffineA[11] = rotatedAffineB[11];
        ifs.set(k, rotatedAffineA);
        // let shear = true;
        // let scale = true;
        // let translate = true;
        // if (shear) {
        //     v[1] = rotatedAffineA[1]; //XY
        //     v[4] = rotatedAffineA[4]; //YX

        //     v[2] = rotatedAffineA[2]; //XZ
        //     v[8] = rotatedAffineA[8]; //ZX

        //     v[6] = rotatedAffineA[6]; //YZ
        //     v[9] = rotatedAffineA[9]; //ZY
        // }
        // if (scale) {
        //     v[0] = rotatedAffineA[0];
        //     v[5] = rotatedAffineA[5];
        //     v[10] = rotatedAffineA[10];
        // }
        
        // if (translate) {
        //     v[3] = rotatedAffineB[3];
        //     v[7] = rotatedAffineB[7];
        //     v[11] = rotatedAffineB[11];
        // }
    });
    return ifs;
}

// for the B translation component only: affine is 12 elements
function rotateAffineB(affine: Float32Array, rad: number, about: string): Float32Array {
    let rotMat: Array<number>;
    if (about==="x") {
        rotMat = [1, 0, 0,
            0, Math.cos(rad), -Math.sin(rad),
            0, Math.sin(rad), Math.cos(rad)];
    } else if (about==="y") {
        rotMat = [Math.cos(rad), 0, Math.sin(rad),
            0, 1, 0,
            -Math.sin(rad), 0, Math.cos(rad)];
    } else {
        rotMat = [Math.cos(rad), -Math.sin(rad), 0,
            Math.sin(rad), Math.cos(rad), 0,
            0, 0, 1];
    }
    return matMul(new Float32Array(rotMat), affine.slice());
}

// for the A scale and shear component only: affine is 12 elements
function rotateAffineA(affine: Float32Array, rad: number, about: string): Float32Array {
    let scaleIdx1; let shearIdx12; let shearIdx13;
    let shearIdx21; let scaleIdx2; let shearIdx23;
    let shearIdx31; let shearIdx32;
    if (about==="x") {
        scaleIdx1 = 10; //Scale Z
        scaleIdx2 = 5; //Scale Y
        shearIdx12 = 9; //ShearZ(Y)
        shearIdx21 = 6; //ShearY(Z)

        shearIdx13 = 4; //ShearY(X) //1 and 2 switched in this case? but not always?
        shearIdx31 = 1; //ShearX(Y)
        shearIdx23 = 8; //ShearZ(X)
        shearIdx32 = 2; //ShearX(Z)
    } else if (about==="y") {
        scaleIdx1 = 0; //Scale X
        scaleIdx2 = 10; //Scale Z
        shearIdx12 = 2; //ShearX(Z)
        shearIdx21 = 8; //ShearZ(X)

        shearIdx13 = 9 //ShearZ(Y) //1 and 2 switched in this case?
        shearIdx31 = 6 //ShearY(Z)
        shearIdx23 = 1 //ShearX(Y)
        shearIdx32 = 4 //ShearY(X)

        // shearIdx13 = 1 //ShearX(Y) //1 and 2 normal
        // shearIdx31 = 4 //ShearY(X)
        // shearIdx23 = 9 //ShearZ(Y)
        // shearIdx32 = 6 //ShearY(Z)
    } else {
        scaleIdx1 = 0; //Scale X
        scaleIdx2 = 5; //Scale Y
        shearIdx12 = 1; //ShearX(Y)
        shearIdx21 = 4; //ShearY(X)

        shearIdx13 = 2; //ShearX(Z)
        shearIdx31 = 8; //ShearZ(X)
        shearIdx23 = 6; //ShearY(Z)
        shearIdx32 = 9; //ShearZ(Y)
    }

    let ret = affine.slice();
    let scaleX = affine[scaleIdx1]; let shearXY = affine[shearIdx12]; let shearXZ = affine[shearIdx13];
    let shearYX = affine[shearIdx21]; let scaleY = affine[scaleIdx2]; let shearYZ = affine[shearIdx23];
    let shearZX = affine[shearIdx31]; let shearZY = affine[shearIdx32];

    const N_WAVE = 2;

    // ADJUSTING FOR ScaleX != ScaleY
    let ampScale = (scaleX-scaleY)/2;
    let vertScale = (scaleX+scaleY)/2;
    ret[scaleIdx1] = ampScale*Math.cos(2*rad) + vertScale //Scale X
    ret[scaleIdx2] = -ampScale*Math.cos(2*rad) + vertScale //Scale Y
    // TODO: one 90deg != two 45 deg (first 45 will make scaleX=ScaleY, then no change)
    // SOLUTION: rotate the points but project onto line connecting (X,Y) and (Y,X): y=()
    // Is it possible that it is regular rotation when you use ShearXY and Shear YX?
    // when you rotate 45 deg and scaleX==scaleY,
    //you need to rely on the augmented shear values to continue changing the scaleX and Y

    ret[shearIdx12] = ampScale*Math.sin(N_WAVE*rad)// + shearXY //ShearXY
    ret[shearIdx21] = ampScale*Math.sin(N_WAVE*rad)// + shearYX //ShearYX
    //TODO: make them diverge negatively on some conditions

    // ADJUSTING FOR Shear XY != -Shear YX
    let ampShear = (shearXY+shearYX)/2;
    let shearXshift = shearXY>shearYX ? Math.PI : 0
    let shearYshift = shearXY<shearYX ? Math.PI : 0
    ret[scaleIdx1] += ampShear*Math.sin(N_WAVE*rad + shearXshift)// + scaleX //ScaleX
    ret[scaleIdx2] += ampShear*Math.sin(N_WAVE*rad + shearYshift)// + scaleY //ScaleY
    ret[shearIdx12] += ampShear*Math.cos(N_WAVE*rad) + ((shearXY-shearYX)/2) //Shear XY
    ret[shearIdx21] += ampShear*Math.cos(N_WAVE*rad) + ((shearYX-shearXY)/2) //Shear YX

    // // ADJUSTING FOR Shear XZ, ZX, YZ, ZY
    // //Shear XZ and Shear YZ
    let rotMat = [Math.cos(rad), -Math.sin(rad),
                    Math.sin(rad), Math.cos(rad)];
    let shearMat = [shearXZ, shearZX, shearYZ, shearZY];
    let rotatedShearMat = matMul(new Float32Array(rotMat), new Float32Array(shearMat));
    ret[shearIdx13] = rotatedShearMat[0];
    ret[shearIdx31] = rotatedShearMat[1];
    ret[shearIdx23] = rotatedShearMat[2];
    ret[shearIdx32] = rotatedShearMat[3];

    return ret;
}

// m1 is sharedDim x sharedDim, m2 is sharedDim x n
function matMul(m1: Float32Array, m2: Float32Array): Float32Array {
    let sharedDim = Math.sqrt(m1.length);
    let m2Dim = m2.length / sharedDim;
    let ret = new Float32Array(m2.length);
    for (let i=0; i<sharedDim; i++) {
        for (let j=0; j<m2Dim; j++) {
            let total = 0;
            for (let k=0; k<sharedDim; k++) {
                // total += m1[i, k] * m1[k, j]
                total += m1[(i*sharedDim)+k] * m2[(k*m2Dim)+j]
            }
            ret[(i*m2Dim)+j] = total;
        }
    }
    return ret
}