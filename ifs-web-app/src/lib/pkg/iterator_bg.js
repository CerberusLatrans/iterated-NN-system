let wasm;
export function __wbg_set_wasm(val) {
    wasm = val;
}


const heap = new Array(128).fill(undefined);

heap.push(undefined, null, true, false);

function getObject(idx) { return heap[idx]; }

let heap_next = heap.length;

function dropObject(idx) {
    if (idx < 132) return;
    heap[idx] = heap_next;
    heap_next = idx;
}

function takeObject(idx) {
    const ret = getObject(idx);
    dropObject(idx);
    return ret;
}

const lTextDecoder = typeof TextDecoder === 'undefined' ? (0, module.require)('util').TextDecoder : TextDecoder;

let cachedTextDecoder = new lTextDecoder('utf-8', { ignoreBOM: true, fatal: true });

cachedTextDecoder.decode();

let cachedUint8Memory0 = null;

function getUint8Memory0() {
    if (cachedUint8Memory0 === null || cachedUint8Memory0.byteLength === 0) {
        cachedUint8Memory0 = new Uint8Array(wasm.memory.buffer);
    }
    return cachedUint8Memory0;
}

function getStringFromWasm0(ptr, len) {
    ptr = ptr >>> 0;
    return cachedTextDecoder.decode(getUint8Memory0().subarray(ptr, ptr + len));
}

function addHeapObject(obj) {
    if (heap_next === heap.length) heap.push(heap.length + 1);
    const idx = heap_next;
    heap_next = heap[idx];

    heap[idx] = obj;
    return idx;
}

let cachedFloat32Memory0 = null;

function getFloat32Memory0() {
    if (cachedFloat32Memory0 === null || cachedFloat32Memory0.byteLength === 0) {
        cachedFloat32Memory0 = new Float32Array(wasm.memory.buffer);
    }
    return cachedFloat32Memory0;
}

let WASM_VECTOR_LEN = 0;

function passArrayF32ToWasm0(arg, malloc) {
    const ptr = malloc(arg.length * 4, 4) >>> 0;
    getFloat32Memory0().set(arg, ptr / 4);
    WASM_VECTOR_LEN = arg.length;
    return ptr;
}

let cachedUint32Memory0 = null;

function getUint32Memory0() {
    if (cachedUint32Memory0 === null || cachedUint32Memory0.byteLength === 0) {
        cachedUint32Memory0 = new Uint32Array(wasm.memory.buffer);
    }
    return cachedUint32Memory0;
}

function passArrayJsValueToWasm0(array, malloc) {
    const ptr = malloc(array.length * 4, 4) >>> 0;
    const mem = getUint32Memory0();
    for (let i = 0; i < array.length; i++) {
        mem[ptr / 4 + i] = addHeapObject(array[i]);
    }
    WASM_VECTOR_LEN = array.length;
    return ptr;
}

function _assertClass(instance, klass) {
    if (!(instance instanceof klass)) {
        throw new Error(`expected instance of ${klass.name}`);
    }
    return instance.ptr;
}

function handleError(f, args) {
    try {
        return f.apply(this, args);
    } catch (e) {
        wasm.__wbindgen_exn_store(addHeapObject(e));
    }
}

const lTextEncoder = typeof TextEncoder === 'undefined' ? (0, module.require)('util').TextEncoder : TextEncoder;

let cachedTextEncoder = new lTextEncoder('utf-8');

const encodeString = (typeof cachedTextEncoder.encodeInto === 'function'
    ? function (arg, view) {
    return cachedTextEncoder.encodeInto(arg, view);
}
    : function (arg, view) {
    const buf = cachedTextEncoder.encode(arg);
    view.set(buf);
    return {
        read: arg.length,
        written: buf.length
    };
});

function passStringToWasm0(arg, malloc, realloc) {

    if (realloc === undefined) {
        const buf = cachedTextEncoder.encode(arg);
        const ptr = malloc(buf.length, 1) >>> 0;
        getUint8Memory0().subarray(ptr, ptr + buf.length).set(buf);
        WASM_VECTOR_LEN = buf.length;
        return ptr;
    }

    let len = arg.length;
    let ptr = malloc(len, 1) >>> 0;

    const mem = getUint8Memory0();

    let offset = 0;

    for (; offset < len; offset++) {
        const code = arg.charCodeAt(offset);
        if (code > 0x7F) break;
        mem[ptr + offset] = code;
    }

    if (offset !== len) {
        if (offset !== 0) {
            arg = arg.slice(offset);
        }
        ptr = realloc(ptr, len, len = offset + arg.length * 3, 1) >>> 0;
        const view = getUint8Memory0().subarray(ptr + offset, ptr + len);
        const ret = encodeString(arg, view);

        offset += ret.written;
        ptr = realloc(ptr, len, offset, 1) >>> 0;
    }

    WASM_VECTOR_LEN = offset;
    return ptr;
}

let cachedInt32Memory0 = null;

function getInt32Memory0() {
    if (cachedInt32Memory0 === null || cachedInt32Memory0.byteLength === 0) {
        cachedInt32Memory0 = new Int32Array(wasm.memory.buffer);
    }
    return cachedInt32Memory0;
}

const AffineTransformationFinalization = (typeof FinalizationRegistry === 'undefined')
    ? { register: () => {}, unregister: () => {} }
    : new FinalizationRegistry(ptr => wasm.__wbg_affinetransformation_free(ptr >>> 0));
/**
* A single affine transformation in 3D space
*/
export class AffineTransformation {

    static __wrap(ptr) {
        ptr = ptr >>> 0;
        const obj = Object.create(AffineTransformation.prototype);
        obj.__wbg_ptr = ptr;
        AffineTransformationFinalization.register(obj, obj.__wbg_ptr, obj);
        return obj;
    }

    static __unwrap(jsValue) {
        if (!(jsValue instanceof AffineTransformation)) {
            return 0;
        }
        return jsValue.__destroy_into_raw();
    }

    __destroy_into_raw() {
        const ptr = this.__wbg_ptr;
        this.__wbg_ptr = 0;
        AffineTransformationFinalization.unregister(this);
        return ptr;
    }

    free() {
        const ptr = this.__destroy_into_raw();
        wasm.__wbg_affinetransformation_free(ptr);
    }
    /**
    * Create a new affine transformation from matrix components
    * @param {Float32Array} x
    * @returns {AffineTransformation}
    */
    static new(x) {
        const ptr0 = passArrayF32ToWasm0(x, wasm.__wbindgen_malloc);
        const len0 = WASM_VECTOR_LEN;
        const ret = wasm.affinetransformation_new(ptr0, len0);
        return AffineTransformation.__wrap(ret);
    }
}

const IteratedFunctionSystemFinalization = (typeof FinalizationRegistry === 'undefined')
    ? { register: () => {}, unregister: () => {} }
    : new FinalizationRegistry(ptr => wasm.__wbg_iteratedfunctionsystem_free(ptr >>> 0));
/**
* The Iterated Function System class
*/
export class IteratedFunctionSystem {

    static __wrap(ptr) {
        ptr = ptr >>> 0;
        const obj = Object.create(IteratedFunctionSystem.prototype);
        obj.__wbg_ptr = ptr;
        IteratedFunctionSystemFinalization.register(obj, obj.__wbg_ptr, obj);
        return obj;
    }

    __destroy_into_raw() {
        const ptr = this.__wbg_ptr;
        this.__wbg_ptr = 0;
        IteratedFunctionSystemFinalization.unregister(this);
        return ptr;
    }

    free() {
        const ptr = this.__destroy_into_raw();
        wasm.__wbg_iteratedfunctionsystem_free(ptr);
    }
    /**
    */
    static init() {
        wasm.iteratedfunctionsystem_init();
    }
    /**
    * Create a new IFS with the given transformations
    * @param {(AffineTransformation)[]} transformations
    * @returns {IteratedFunctionSystem}
    */
    static new(transformations) {
        const ptr0 = passArrayJsValueToWasm0(transformations, wasm.__wbindgen_malloc);
        const len0 = WASM_VECTOR_LEN;
        const ret = wasm.iteratedfunctionsystem_new(ptr0, len0);
        return IteratedFunctionSystem.__wrap(ret);
    }
    /**
    * @param {(AffineTransformation)[]} transformations
    * @param {Float32Array} probabilities
    * @returns {IteratedFunctionSystem}
    */
    static new_from_probabilities(transformations, probabilities) {
        const ptr0 = passArrayJsValueToWasm0(transformations, wasm.__wbindgen_malloc);
        const len0 = WASM_VECTOR_LEN;
        const ptr1 = passArrayF32ToWasm0(probabilities, wasm.__wbindgen_malloc);
        const len1 = WASM_VECTOR_LEN;
        const ret = wasm.iteratedfunctionsystem_new_from_probabilities(ptr0, len0, ptr1, len1);
        return IteratedFunctionSystem.__wrap(ret);
    }
    /**
    * @param {(AffineTransformation)[]} transformations
    * @param {MarkovChain} chain
    * @returns {IteratedFunctionSystem}
    */
    static new_from_markov(transformations, chain) {
        const ptr0 = passArrayJsValueToWasm0(transformations, wasm.__wbindgen_malloc);
        const len0 = WASM_VECTOR_LEN;
        _assertClass(chain, MarkovChain);
        var ptr1 = chain.__destroy_into_raw();
        const ret = wasm.iteratedfunctionsystem_new_from_markov(ptr0, len0, ptr1);
        return IteratedFunctionSystem.__wrap(ret);
    }
    /**
    * Generate points using the IFS
    * @param {number} num_points
    * @returns {PtrTuple}
    */
    generate_colors(num_points) {
        const ret = wasm.iteratedfunctionsystem_generate_colors(this.__wbg_ptr, num_points);
        return PtrTuple.__wrap(ret);
    }
    /**
    * Generate points using the IFS
    * @param {number} num_points
    * @returns {number}
    */
    generate(num_points) {
        const ret = wasm.iteratedfunctionsystem_generate(this.__wbg_ptr, num_points);
        return ret >>> 0;
    }
}

const MarkovChainFinalization = (typeof FinalizationRegistry === 'undefined')
    ? { register: () => {}, unregister: () => {} }
    : new FinalizationRegistry(ptr => wasm.__wbg_markovchain_free(ptr >>> 0));
/**
*/
export class MarkovChain {

    static __wrap(ptr) {
        ptr = ptr >>> 0;
        const obj = Object.create(MarkovChain.prototype);
        obj.__wbg_ptr = ptr;
        MarkovChainFinalization.register(obj, obj.__wbg_ptr, obj);
        return obj;
    }

    __destroy_into_raw() {
        const ptr = this.__wbg_ptr;
        this.__wbg_ptr = 0;
        MarkovChainFinalization.unregister(this);
        return ptr;
    }

    free() {
        const ptr = this.__destroy_into_raw();
        wasm.__wbg_markovchain_free(ptr);
    }
    /**
    * @param {Float32Array} flat_matrix
    * @param {number} n
    * @returns {MarkovChain}
    */
    static new(flat_matrix, n) {
        const ptr0 = passArrayF32ToWasm0(flat_matrix, wasm.__wbindgen_malloc);
        const len0 = WASM_VECTOR_LEN;
        const ret = wasm.markovchain_new(ptr0, len0, n);
        return MarkovChain.__wrap(ret);
    }
    /**
    * @param {Float32Array} probabilities
    * @returns {MarkovChain}
    */
    static from_probabilities(probabilities) {
        const ptr0 = passArrayF32ToWasm0(probabilities, wasm.__wbindgen_malloc);
        const len0 = WASM_VECTOR_LEN;
        const ret = wasm.markovchain_from_probabilities(ptr0, len0);
        return MarkovChain.__wrap(ret);
    }
}

const PtrTupleFinalization = (typeof FinalizationRegistry === 'undefined')
    ? { register: () => {}, unregister: () => {} }
    : new FinalizationRegistry(ptr => wasm.__wbg_ptrtuple_free(ptr >>> 0));
/**
* Pointer Tuple class (to export to JS frontend)
*/
export class PtrTuple {

    static __wrap(ptr) {
        ptr = ptr >>> 0;
        const obj = Object.create(PtrTuple.prototype);
        obj.__wbg_ptr = ptr;
        PtrTupleFinalization.register(obj, obj.__wbg_ptr, obj);
        return obj;
    }

    __destroy_into_raw() {
        const ptr = this.__wbg_ptr;
        this.__wbg_ptr = 0;
        PtrTupleFinalization.unregister(this);
        return ptr;
    }

    free() {
        const ptr = this.__destroy_into_raw();
        wasm.__wbg_ptrtuple_free(ptr);
    }
    /**
    * @returns {number}
    */
    get points_ptr() {
        const ret = wasm.__wbg_get_ptrtuple_points_ptr(this.__wbg_ptr);
        return ret >>> 0;
    }
    /**
    * @param {number} arg0
    */
    set points_ptr(arg0) {
        wasm.__wbg_set_ptrtuple_points_ptr(this.__wbg_ptr, arg0);
    }
    /**
    * @returns {number}
    */
    get colors_ptr() {
        const ret = wasm.__wbg_get_ptrtuple_colors_ptr(this.__wbg_ptr);
        return ret >>> 0;
    }
    /**
    * @param {number} arg0
    */
    set colors_ptr(arg0) {
        wasm.__wbg_set_ptrtuple_colors_ptr(this.__wbg_ptr, arg0);
    }
    /**
    * @returns {number}
    */
    get color_map() {
        const ret = wasm.__wbg_get_ptrtuple_color_map(this.__wbg_ptr);
        return ret >>> 0;
    }
    /**
    * @param {number} arg0
    */
    set color_map(arg0) {
        wasm.__wbg_set_ptrtuple_color_map(this.__wbg_ptr, arg0);
    }
}

export function __wbg_affinetransformation_unwrap(arg0) {
    const ret = AffineTransformation.__unwrap(takeObject(arg0));
    return ret;
};

export function __wbindgen_object_drop_ref(arg0) {
    takeObject(arg0);
};

export function __wbg_crypto_1d1f22824a6a080c(arg0) {
    const ret = getObject(arg0).crypto;
    return addHeapObject(ret);
};

export function __wbindgen_is_object(arg0) {
    const val = getObject(arg0);
    const ret = typeof(val) === 'object' && val !== null;
    return ret;
};

export function __wbg_process_4a72847cc503995b(arg0) {
    const ret = getObject(arg0).process;
    return addHeapObject(ret);
};

export function __wbg_versions_f686565e586dd935(arg0) {
    const ret = getObject(arg0).versions;
    return addHeapObject(ret);
};

export function __wbg_node_104a2ff8d6ea03a2(arg0) {
    const ret = getObject(arg0).node;
    return addHeapObject(ret);
};

export function __wbindgen_is_string(arg0) {
    const ret = typeof(getObject(arg0)) === 'string';
    return ret;
};

export function __wbg_require_cca90b1a94a0255b() { return handleError(function () {
    const ret = module.require;
    return addHeapObject(ret);
}, arguments) };

export function __wbindgen_is_function(arg0) {
    const ret = typeof(getObject(arg0)) === 'function';
    return ret;
};

export function __wbindgen_string_new(arg0, arg1) {
    const ret = getStringFromWasm0(arg0, arg1);
    return addHeapObject(ret);
};

export function __wbg_msCrypto_eb05e62b530a1508(arg0) {
    const ret = getObject(arg0).msCrypto;
    return addHeapObject(ret);
};

export function __wbg_randomFillSync_5c9c955aa56b6049() { return handleError(function (arg0, arg1) {
    getObject(arg0).randomFillSync(takeObject(arg1));
}, arguments) };

export function __wbg_getRandomValues_3aa56aa6edec874c() { return handleError(function (arg0, arg1) {
    getObject(arg0).getRandomValues(getObject(arg1));
}, arguments) };

export function __wbg_newnoargs_e258087cd0daa0ea(arg0, arg1) {
    const ret = new Function(getStringFromWasm0(arg0, arg1));
    return addHeapObject(ret);
};

export function __wbg_call_27c0f87801dedf93() { return handleError(function (arg0, arg1) {
    const ret = getObject(arg0).call(getObject(arg1));
    return addHeapObject(ret);
}, arguments) };

export function __wbindgen_object_clone_ref(arg0) {
    const ret = getObject(arg0);
    return addHeapObject(ret);
};

export function __wbg_self_ce0dbfc45cf2f5be() { return handleError(function () {
    const ret = self.self;
    return addHeapObject(ret);
}, arguments) };

export function __wbg_window_c6fb939a7f436783() { return handleError(function () {
    const ret = window.window;
    return addHeapObject(ret);
}, arguments) };

export function __wbg_globalThis_d1e6af4856ba331b() { return handleError(function () {
    const ret = globalThis.globalThis;
    return addHeapObject(ret);
}, arguments) };

export function __wbg_global_207b558942527489() { return handleError(function () {
    const ret = global.global;
    return addHeapObject(ret);
}, arguments) };

export function __wbindgen_is_undefined(arg0) {
    const ret = getObject(arg0) === undefined;
    return ret;
};

export function __wbg_call_b3ca7c6051f9bec1() { return handleError(function (arg0, arg1, arg2) {
    const ret = getObject(arg0).call(getObject(arg1), getObject(arg2));
    return addHeapObject(ret);
}, arguments) };

export function __wbg_buffer_12d079cc21e14bdb(arg0) {
    const ret = getObject(arg0).buffer;
    return addHeapObject(ret);
};

export function __wbg_newwithbyteoffsetandlength_aa4a17c33a06e5cb(arg0, arg1, arg2) {
    const ret = new Uint8Array(getObject(arg0), arg1 >>> 0, arg2 >>> 0);
    return addHeapObject(ret);
};

export function __wbg_new_63b92bc8671ed464(arg0) {
    const ret = new Uint8Array(getObject(arg0));
    return addHeapObject(ret);
};

export function __wbg_set_a47bac70306a19a7(arg0, arg1, arg2) {
    getObject(arg0).set(getObject(arg1), arg2 >>> 0);
};

export function __wbg_newwithlength_e9b4878cebadb3d3(arg0) {
    const ret = new Uint8Array(arg0 >>> 0);
    return addHeapObject(ret);
};

export function __wbg_subarray_a1f73cd4b5b42fe1(arg0, arg1, arg2) {
    const ret = getObject(arg0).subarray(arg1 >>> 0, arg2 >>> 0);
    return addHeapObject(ret);
};

export function __wbg_new_abda76e883ba8a5f() {
    const ret = new Error();
    return addHeapObject(ret);
};

export function __wbg_stack_658279fe44541cf6(arg0, arg1) {
    const ret = getObject(arg1).stack;
    const ptr1 = passStringToWasm0(ret, wasm.__wbindgen_malloc, wasm.__wbindgen_realloc);
    const len1 = WASM_VECTOR_LEN;
    getInt32Memory0()[arg0 / 4 + 1] = len1;
    getInt32Memory0()[arg0 / 4 + 0] = ptr1;
};

export function __wbg_error_f851667af71bcfc6(arg0, arg1) {
    let deferred0_0;
    let deferred0_1;
    try {
        deferred0_0 = arg0;
        deferred0_1 = arg1;
        console.error(getStringFromWasm0(arg0, arg1));
    } finally {
        wasm.__wbindgen_free(deferred0_0, deferred0_1, 1);
    }
};

export function __wbindgen_throw(arg0, arg1) {
    throw new Error(getStringFromWasm0(arg0, arg1));
};

export function __wbindgen_memory() {
    const ret = wasm.memory;
    return addHeapObject(ret);
};

