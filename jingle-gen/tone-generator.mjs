import { AudioContext } from 'node-web-audio-api';
import { Writable } from 'stream';
import wav from 'wav';

// Constants
const MAX_TONES = 3;
const TONE_DURATION = 0.3; // Duration in seconds

// Helper function to map vector components to frequencies
function mapToFrequency(value) {
    const minFreq = 250; // Minimum frequency in Hz
    const maxFreq = 2500; // Maximum frequency in Hz
    return minFreq + (maxFreq - minFreq) * value;
}

// Helper function to reduce a 128-component vector to a smaller number of sounds
function reduceVector(vector, maxTones) {
    const step = Math.floor(vector.length / maxTones);
    const reducedVector = [];
    for (let i = 0; i < vector.length; i += step) {
        reducedVector.push(vector[i]);
    }
    return reducedVector;
}

// Helper function to apply an ADSR envelope to the sound
// Goal is to make the sound more pleasant to listen too
function applyEnvelope(sampleRate, duration, channelData) {
    const attack = 0.01 * duration; // 10% of the duration
    const decay = 0.1 * duration; // 10% of the duration
    const sustain = 0.7 * duration; // 70% of the duration
    const release = 0.05 * duration; // 10% of the duration

    const attackEnd = attack * sampleRate;
    const decayEnd = (attack + decay) * sampleRate;
    const sustainEnd = (attack + decay + sustain) * sampleRate;
    const releaseEnd = (attack + decay + sustain + release) * sampleRate;

    for (let i = 0; i < channelData.length; i++) {
        if (i < attackEnd) {
            // Attack phase
            channelData[i] *= i / attackEnd;
        } else if (i < decayEnd) {
            // Decay phase
            channelData[i] *= 1 - ((i - attackEnd) / (decayEnd - attackEnd)) * 0.5; // Decay to 50% amplitude
        } else if (i < sustainEnd) {
            // Sustain phase
            channelData[i] *= 0.5; // Sustain at 50% amplitude
        } else if (i < releaseEnd) {
            // Release phase
            channelData[i] *= 0.5 * (1 - (i - sustainEnd) / (releaseEnd - sustainEnd)); // Release to 0 amplitude
        } else {
            // After release phase
            channelData[i] = 0;
        }
    }
}

// Helper unction to generate a jingle from a 128-component vector
async function generateJingle(vector) {
    // Currently only supports 128-component row vectors
    if (vector.length !== 128) {
        throw new Error('Vector expected to have 128 components');
    }

    const context = new AudioContext();
    const sampleRate = context.sampleRate;
    const duration = vector.length * 0.1; // Duration in seconds
    const buffer = context.createBuffer(1, sampleRate * duration, sampleRate);
    const channelData = buffer.getChannelData(0);

    // Map each component to a frequency and generate the tone
    for (let i = 0; i < vector.length; i++) {
        const frequency = mapToFrequency(vector[i]);
        const startTime = i * 0.1 * sampleRate;
        const endTime = (i + 1) * 0.1 * sampleRate;
        for (let j = startTime; j < endTime; j++) {
            channelData[j] = Math.sin(2 * Math.PI * frequency * (j / sampleRate));
        }
    }

    // Apply the envelope to the sound to achieve retrieved tone
    applyEnvelope(sampleRate, duration, channelData);

    // Create a WAV file
    const fileWriter = new wav.FileWriter('jingle.wav', {
        channels: 1,
        sampleRate: sampleRate,
        bitDepth: 16
    });

    const audioStream = new Writable({
        write(chunk, encoding, callback) {
            fileWriter.write(chunk);
            callback();
        }
    });

    // A buffer is used as opposed to web audio context
    // UPDATE: No longer generating from Tone.js
    const audioBuffer = Buffer.from(buffer.getChannelData(0).buffer);
    audioStream.write(audioBuffer);
    audioStream.end(() => {
        fileWriter.end();
        console.log('Jingle generated and saved as jingle.wav');
    });

    // Play the sound
    const bufferSource = context.createBufferSource();
    bufferSource.buffer = buffer;
    bufferSource.connect(context.destination);
    bufferSource.start();
}

// Function to generate a reduced jingle from a 128-component vector
async function generateReducedJingle(vector) {
    // Like before, a 128-component row vector is still expected to be reduced
    if (vector.length !== 128) {
        throw new Error('Vector expected to have have 128 components');
    }

    const reducedVector = reduceVector(vector, MAX_TONES);

    const context = new AudioContext();
    const sampleRate = context.sampleRate;
    const duration = reducedVector.length * TONE_DURATION; // Duration in seconds
    const buffer = context.createBuffer(1, sampleRate * duration, sampleRate);
    const channelData = buffer.getChannelData(0);

    // Map each component to a frequency and generate the tone
    for (let i = 0; i < reducedVector.length; i++) {
        const frequency = mapToFrequency(reducedVector[i]);
        const startTime = i * TONE_DURATION * sampleRate;
        const endTime = (i + 1) * TONE_DURATION * sampleRate;
        for (let j = startTime; j < endTime; j++) {
            channelData[j] = Math.sin(2 * Math.PI * frequency * (j / sampleRate));
        }
    }

    // Apply the envelope to the sound (not redundant if frequencies are regenerated)
    applyEnvelope(sampleRate, duration, channelData);

    // Create a WAV file
    const fileWriter = new wav.FileWriter('reduced_jingle.wav', {
        channels: 1,
        sampleRate: sampleRate,
        bitDepth: 16
    });

    const audioStream = new Writable({
        write(chunk, encoding, callback) {
            fileWriter.write(chunk);
            callback();
        }
    });

    const audioBuffer = Buffer.from(buffer.getChannelData(0).buffer);
    audioStream.write(audioBuffer);
    audioStream.end(() => {
        fileWriter.end();
        console.log('Reduced jingle generated and saved as reduced_jingle.wav');
    });

    // Play the sound
    const bufferSource = context.createBufferSource();
    bufferSource.buffer = buffer;
    bufferSource.connect(context.destination);
    bufferSource.start();
}

// Export the functions
export { mapToFrequency, generateJingle, generateReducedJingle };
