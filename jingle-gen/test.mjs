import { generateReducedJingle } from './tone-generator.mjs';

const vector = Array.from({ length: 128 }, () => Math.random()); // Example vector with random values

generateReducedJingle(vector).then(() => {
    console.log('Reduced jingle generated and saved as reduced_jingle.wav');

    // Wait for 5 seconds then generate the jingle from the vector again and play it
    setTimeout(() => {
        generateReducedJingle(vector).then(() => {
            console.log('Reduced jingle generated and saved as reduced_jingle.wav');
        }).catch(error => {
            console.error('Error generating reduced jingle:', error);
        });
    }, 5000);
}).catch(error => {
    console.error('Error generating reduced jingle:', error);
});
