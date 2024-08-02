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

export function rotateIFS(
    ifs: Map<number, Float32Array>,
    rad: number,
    about: string
): Map<number, Float32Array> {
    ifs.forEach((v, k) => {
        let rotatedAffineB = rotateAffineB(v, rad, about);
        let rotatedAffineA = rotateAffineA(v, rad, about);
        let shear = true;
        let scale = true;
        let translate = true;
        if (shear) {
            v[1] = rotatedAffineA[1]; //XY
            v[4] = rotatedAffineA[4]; //YX

            //v[2] = rotatedAffineA[2]; //XZ
            //v[8] = rotatedAffineA[8]; //ZX

            //v[6] = rotatedAffineA[6]; //YZ
            //v[9] = rotatedAffineA[9]; //ZY
        }
        if (scale) {
            v[0] = rotatedAffineA[0];
            v[5] = rotatedAffineA[5];
            //v[10] = rotatedAffineA[10];
        }
        
        if (translate) {
            v[3] = rotatedAffineB[3];
            v[7] = rotatedAffineB[7];
            v[11] = rotatedAffineB[11];
        }
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
    return matMul(new Float32Array(rotMat), affine);
}

// for the A scale and shear component only: affine is 12 elements
function rotateAffineA(affine: Float32Array, rad: number, about: string): Float32Array {
    let ret = new Float32Array(12);

    let scaleX = affine[0];
    let scaleY = affine[5];
    let shearX = affine[1];
    let shearY = affine[4];

    const N_WAVE = 2;

    // ADJUSTING FOR ScaleX != ScaleY
    let ampScale = Math.abs(scaleX-scaleY)/2;
    let scaleXshift = scaleX<scaleY ? Math.PI : 0
    let scaleYshift = scaleX>scaleY ? Math.PI : 0
    //Scale X and Scale Y
    let vertScale = (scaleX+scaleY)/2;
    ret[0] = ampScale*Math.cos(N_WAVE*rad + scaleXshift) + vertScale
    ret[5] = ampScale*Math.cos(N_WAVE*rad + scaleYshift) + vertScale
    //Shear X and Shear Y
    ret[1] = ampScale*Math.sin(N_WAVE*rad)// + shearX
    ret[4] = ampScale*Math.sin(N_WAVE*rad)// + shearY

    // ADJUSTING FOR ShearX != -ShearY
    let ampShear = (shearX+shearY)/2;
    //Scale X and Scale Y
    let shearXshift = shearX>shearY ? Math.PI : 0
    let shearYshift = shearX<shearY ? Math.PI : 0
    ret[0] += ampShear*Math.sin(N_WAVE*rad + shearXshift)// + scaleX
    ret[5] += ampShear*Math.sin(N_WAVE*rad + shearYshift)// + scaleY
    //Shear X and Shear Y
    ret[1] += ampShear*Math.cos(N_WAVE*rad) + ((shearX-shearY)/2)
    ret[4] += ampShear*Math.cos(N_WAVE*rad) + ((shearY-shearX)/2)

    return ret;
}

// m1 is 3x3, m2 is 3x4
function matMul(m1: Float32Array, m2: Float32Array): Float32Array {
    let ret = new Float32Array(12);
    for (let i=0; i<3; i++) {
        for (let j=0; j<4; j++) {
            let total = 0;
            for (let k=0; k<3; k++) {
                // total += m1[i, k] * m1[k, j]
                total += m1[(i*3)+k] * m2[(k*4)+j]
            }
            ret[(i*4)+j] = total;
        }
    }
    return ret
}