import { Tensor, InferenceSession } from "onnxruntime-web";
import * as ort from "onnxruntime-web/webgpu";
import { pipeline, AutoModelForSeq2SeqLM, AutoTokenizer, Seq2SeqLMOutput } from '@xenova/transformers';

async function runT5(wee: string) {
    console.log(wee)
    const t5Model = 'Xenova/t5-small';
    let tokenizer = await AutoTokenizer.from_pretrained(t5Model);
    let model = await AutoModelForSeq2SeqLM.from_pretrained(t5Model);
    let tokens = tokenizer(wee);
    console.log('TOKENS', tokens)
    let result = await model.generate(tokens['input_ids']);
    console.log('RESULT', result)
    let output = new Seq2SeqLMOutput(result)
    console.log(output)
    let embedding = output.encoder_outputs;
    console.log(embedding)
    let decoded = tokenizer.decode(result[0], { skip_special_tokens: true });
    console.log("DECODED", decoded)
    return embedding;
  }

async function runT5ONNX(text: string) {
    const t5Model = 'Xenova/t5-small';
    let tokenizer = await AutoTokenizer.from_pretrained(t5Model);
    let tokens: Tensor = tokenizer(text);

    const t5Path = "../models/t5-encoder-12.onnx"
    const session = await InferenceSession.create(t5Path, { executionProviders: ['webgpu'], graphOptimizationLevel: 'all' });
    const feeds: Record<string, ort.Tensor> = {};
    feeds[session.inputNames[0]] = tokens
    const outputData = await session.run(feeds);
    const embedding = outputData[session.outputNames[0]];
    return embedding
}

//async function runIFSNet(encoding: Tensor) {
//    const ifsNetPath = "../models/t5-encoder-12.onnx"
//    const session = await InferenceSession.create(t5Path, { executionProviders: ['webGL'], graphOptimizationLevel: 'all' });
//    const feeds: Record<string, ort.Tensor> = {};
//    feeds[session.inputNames[0]] = preprocessedData
//    
//    const outputData = await session.run({ inputName : text});
//    const output = outputData[session.outputNames[0]];
//    return output
//}


export async function runInference(text: string) {
    //let encoding = await runT5ONNX(text);
    let encoding: Tensor = await runT5ONNX(text);
    //let prediction = await runIFSNet(encoding);
    return encoding
}