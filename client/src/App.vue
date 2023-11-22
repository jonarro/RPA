<script setup lang="ts">
import Hero from './components/Hero.vue';
import { ref } from 'vue';

const kerword = ref('');
const location = ref('');
const is_search = ref(false);
const finalPage = ref<number>(1);
const BASE_URL = 'http://localhost:5000/api/v2';

const makeSearch = async () => {
	const data = {
		keyword: kerword.value,
		location: location.value,
		final_page: finalPage.value
	};
	console.log('data', data);

	const url = `${BASE_URL}/people`;

	await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded'
		},
		body: new URLSearchParams(data as any)
	}).then(res => res.json());

	alert('Iniciando busqueda de perfiles');
};

const urls = ref(['']);
const addUrl = () => {
	urls.value.push('');
};
const removeUrl = (index: number) => {
	urls.value.splice(index, 1);
};

const searchProfiles = async () => {
	const profiles_to_search: string[] = [];
	urls.value.forEach(url => {
		if (url !== '') {
			profiles_to_search.push(url);
		}
	});
	const url = `${BASE_URL}/people`;

	const data = {
		profiles_to_search,
		is_search: true
	};
	console.log('data', data);

	await fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/x-www-form-urlencoded'
		},
		body: new URLSearchParams(data as any)
	}).then(res => res.json());

	alert('Iniciando busqueda de perfiles');
};
</script>

<template>
	<main>
		<Hero />
		<div class="flex flex-col py-8 px-8">
			<h1 class="text-4xl text-[#7855FD]">Busqueda de Talento</h1>
			<button
				class="bg-[#7855FD] hover:bg-[#7855FD] text-white font-bold py-2 px-4 rounded mt-4"
				@click="is_search = !is_search"
			>
				Buscar por urls
			</button>
		</div>

		<div
			class="flex flex-col py-8 px-8 justify-center items-center w-screen"
			v-if="!is_search"
		>
			<form
				class="flex flex-col w-screen p-8 justify-center items-center"
				@submit.prevent="makeSearch"
			>
				<label
					class="block text-[#7855FD] text-sm font-bold mb-2"
					for="keyword"
				>
					Puesto
				</label>
				<input
					id="keyword"
					class="border-2 border-[#7855FD] w-2/3 mb-4 rounded-md h-10 bg-white px-4"
					placeholder="Desarrollador Frontend"
					type="text"
					v-model="kerword"
				/>
				<label
					for="location"
					class="block text-[#7855FD] text-sm font-bold mb-2"
				>
					Ubicación
				</label>
				<input
					id="location"
					class="border-2 border-[#7855FD] w-2/3 mb-4 rounded-md h-10 bg-white px-4"
					type="text"
					placeholder="Ciudad de México"
					v-model="location"
				/>

				<label
					for="finalPage"
					class="block text-[#7855FD] text-sm font-bold mb-2"
				>
					Paginas a buscar
				</label>
				<input
					id="finalPage"
					class="border-2 border-[#7855FD] w-2/3 mb-4 rounded-md h-10 bg-white px-4"
					type="number"
					min="1"
					max="100"
					placeholder="1"
					v-model="finalPage"
				/>
				<div>
					<button
						class="bg-[#7855FD] hover:bg-[#7855FD] text-white font-bold py-2 px-4 rounded"
					>
						Buscar
					</button>
				</div>
			</form>
		</div>

		<div
			class="flex flex-col py-8 px-8 justify-center items-center w-screen"
			v-if="is_search"
		>
			<h1>Buscar por url de linkedin</h1>
			<div>
				<button
					class="bg-[#7855FD] hover:bg-[#7855FD] text-white font-bold py-2 px-4 rounded my-4"
					@click="searchProfiles"
				>
					Buscar perfiles
				</button>
			</div>
			<div
				v-for="(url, index) in urls"
				class="flex flex-row w-screen px-8"
				:key="index"
			>
				<input
					type="text"
					:key="url"
					v-model="urls[index]"
					class="border-2 border-[#7855FD] w-2/3 mb-1 rounded-md h-10 bg-white px-4"
					placeholder="htts//linkedin:in/"
				/>
				<button
					class="bg-[#7855FD] hover:bg-[#7855FD] text-white font-bold rounded-md w-9 mb-1"
					@click="
						index === urls.length - 1 ? addUrl() : removeUrl(index)
					"
				>
					{{ index === urls.length - 1 ? '+' : '-' }}
				</button>
			</div>
		</div>
	</main>
</template>
