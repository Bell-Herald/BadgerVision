# Jingle-Gen (Tone Generator)

A simple package to convert a 128-component vector into a short audio jingle using the `node-web-audio-api` library.

## Installation

```sh
npm install node-web-audio-api wav
```

## Functions

`generateJingle(vector)`
Generates a jingle from a 128-component vector and saves it as a `.wav` file.

- Parameters:
    - vector: An array of 128 numbers. Each number should be between 0 and 1.
- Returns:
    - A promise that resolves when the jingle has been generated and saved as a `.wav` file.

`mapToFrequency(value)`
Maps a value to a frequency between 200 Hz and 2000 Hz.

- Parameters:
    - value: A number between 0 and 1.
- Returns:
    - A frequency in Hz corresponding to the input value.

## Usage

```js
import { generateJingle } from './tone-generator.mjs';

const vector = Array.from({ length: 128 }, () => Math.random()); // Example vector with random values
generateJingle(vector).then(() => {
    console.log('Jingle generated and saved as jingle.wav');
}).catch(error => {
    console.error('Error generating jingle:', error);
});
```
