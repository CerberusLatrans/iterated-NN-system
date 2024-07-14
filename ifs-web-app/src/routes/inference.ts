import { Tensor, InferenceSession } from "onnxruntime-web";//webgpu
import * as ort from "onnxruntime-web";
import { pipeline, AutoModelForSeq2SeqLM, AutoTokenizer, Seq2SeqLMOutput} from '@xenova/transformers';

const t5Model = 'Xenova/t5-small';
let tokenizer = await AutoTokenizer.from_pretrained(t5Model);
const t5Path = "./models/t5_encoder_model_quantized.onnx"
const ifsnet_model_name = "IFSNET_arity=4_ep=100_LR=0.001_nsamples=3"
const ifsNetPath = "../models/"+ifsnet_model_name+".onnx"
const device = ort.env.webgpu.device;
const EMBEDDING_SIZE = 512;

async function runT5EmbeddingHF(wee: string) {
    let model = await AutoModelForSeq2SeqLM.from_pretrained(t5Model);
    let tokens = tokenizer(wee);
    let result = await model.generate(tokens['input_ids']);
    let output = new Seq2SeqLMOutput(result)
    let embedding = output.encoder_outputs;
    let decoded = tokenizer.decode(result[0], { skip_special_tokens: true });
    return embedding;
  }

async function runT5Embedding(dataTensor: Tensor, attentionMaskTensor: Tensor) {
    const start = new Date();
    const session = await InferenceSession.create(t5Path, {
        executionProviders: ['webgpu', 'wasm'],
        graphOptimizationLevel: 'all',
        preferredOutputLocation: 'gpu-buffer'});

    const feeds: Record<string, Tensor> = {};
    //DataLocation: "none" | "cpu" | "cpu-pinned" | "texture" | "gpu-buffer"
    dataTensor.location = 'cpu'
    attentionMaskTensor.location = 'cpu'
    feeds['input_ids'] = dataTensor;
    feeds['attention_mask'] = attentionMaskTensor;

    //const fetches: Record<string, Tensor> = {};
    //let gpuBuffer = device.createBuffer({
    //    usage: GPUBufferUsage.COPY_SRC | GPUBufferUsage.COPY_DST | GPUBufferUsage.STORAGE,
    //    size: Math.ceil(bufferSize / 16) * 16 /* align to 16 bytes */
    //});
    //let gpuTensor = Tensor.fromGpuBuffer(gpuBuffer, { dataType: 'float32', dims: [512})
    //fetches[session.outputNames[0]] = gpuTensor;
    const outputData = await session.run(feeds)//, fetches);
    const embedding = outputData[session.outputNames[0]];
    console.log('EMBEDDING TIME: ', (new Date().getTime() - start.getTime())/1000)
    return embedding
}
async function runIFSNet(embedding: Tensor) {
    const start = new Date();
    const session = await InferenceSession.create(ifsNetPath, { executionProviders: ['wasm'], graphOptimizationLevel: 'all' });
    const feeds: Record<string, ort.Tensor> = {};
    feeds[session.inputNames[0]] = embedding
    const outputData = await session.run(feeds);
    const ifs = outputData[session.outputNames[0]];
    console.log('IFSNET TIME: ', (new Date().getTime() - start.getTime())/1000)
    return ifs
}


export async function runInference(text: string) {
    const start = new Date();
    let tokens = tokenizer(text, {"return_tensor":true});
    let embeddings: Tensor = await runT5Embedding(tokens['input_ids'], tokens['attention_mask']);
    //let reshaped = embeddings.reshape()
    const avgStart = new Date();
    let n = embeddings.dims[1] // dims = [1, n, 512]
    //console.log(embeddings, n)
    let embeddingsArray = await embeddings.getData()
    let avgEmbedding = new Float32Array(EMBEDDING_SIZE)
    for (let i=0; i<EMBEDDING_SIZE; i++) {
        let total = 0
        for (let j=0; j<n; j++) {
            total += embeddingsArray[i+(j*EMBEDDING_SIZE)]
        }
        avgEmbedding[i] = total / n
    }
    let avgEmbeddingTensor = new Tensor('float32', avgEmbedding, [EMBEDDING_SIZE])
    console.log('AVGING TIME: ', (new Date().getTime() - avgStart.getTime())/1000)
    let ifsTensor = await runIFSNet(avgEmbeddingTensor);
    let ifsArray = ifsTensor.getData()
    console.log('TOTAL TIME: ', (new Date().getTime() - start.getTime())/1000)
    return ifsArray
}

export function ifsFromArray(ifsArray: Float32Array) {
    const affineDim = 12;
    let ifs = new Map<number, Float32Array>();
    let arity = Math.floor(ifsArray.length/affineDim)
    for (let i=0; i<arity; i++) {
        ifs.set(i, ifsArray.slice((i*affineDim), (i*affineDim)+affineDim))
    }
    return ifs
}