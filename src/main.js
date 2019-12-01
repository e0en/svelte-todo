import App from './App.svelte';

import '../node_modules/bulma/bulma.sass'
const frontendPath = require('../settings.js').frontendPath

const app = new App({
	target: document.body,
});

export default app;

(function () { 
	if ('serviceWorker' in navigator) {
		navigator.serviceWorker.register('./service-worker.js', {scope: frontendPath})
			.then(() => console.log('Service Worker registered successfully.'))
			.catch(error => console.log('Service Worker registration failed:', error));
	}
})();
