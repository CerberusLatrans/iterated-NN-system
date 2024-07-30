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

export function scale(ifs: Map<number, Float32Array>, factor: number) {
    let scaledIfs = new Map();
    ifs.forEach((v, k) => {
        v[3] = v[3]*factor
        v[7] = v[7]*factor
        v[11] = v[11]*factor
        scaledIfs.set(k, v);
    });
    return scaledIfs;
}