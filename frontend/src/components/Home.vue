<template>
    <div class="d-grid min-vh-100" style="grid-template-columns: 250px 1fr;">
        <div class="h-100">

        </div>
        <div class="position-fixed h-100 bg-dark text-white p-3 d-flex flex-column justify-content-between">
            <div>
                <div class="sidebar-header border-bottom border-dark-subtle px-4 pb-2 my-5">
                    <h2>Parking</h2>
                    <h5 class="text-white-50">{{ currentParking.name }}</h5>
                </div>
                <div class="menu-item active" @click="toggleMenuItem($event)">Dashboard</div>
                <div class="menu-item" @click="toggleMenuItem($event)">Vue du parking</div>
                <br>
                <br>
                <br>
                <button class="btn btn-primary menu-item" @click="bookFirstSpot()">Reserver une place</button>
            </div>
            <div>
                <div class="btn-group dropup mb-3">
                    <button type="button" class="btn btn-danger dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                        Debug
                    </button>
                    <ul class="dropdown-menu">
                        <li><button type="button" class="dropdown-item" @click="bookAll()">Réserver tout</button></li>
                        <li><button type="button" class="dropdown-item" @click="unBookAll()">Libérer tout</button></li>
                    </ul>
                </div>
                <div>
                    Template utilisé
                    <a href="https://codepen.io/romain-tortosa/pen/vEBdxMP">ici</a>
                </div>
            </div>
        </div>
        
        <div class="px-5 pt-5">
            <div class="d-grid mb-3" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                <div class="p-4 bg-dark text-white shadow-sm rounded-3">
                    <h5 class="text-white-50 mb-2">Statut du parking</h5>
                    <h2 class="value">{{ freeSpots.length > 0 ? "OUVERT" : "COMPLET" }}</h2>
                </div>
                <div class="p-4 bg-dark text-white shadow-sm rounded-3">
                    <h5 class="text-white-50 mb-2">Places libres</h5>
                    <h2 class="value">{{ freeSpots.length }}</h2>
                </div>
                <div class="p-4 bg-dark text-white shadow-sm rounded-3">
                    <h5 class="text-white-50 mb-2">Places occupées</h5>
                    <h2 class="value">{{ occupiedSpots.length }}</h2>
                </div>
                <div class="p-4 bg-dark text-white shadow-sm rounded-3">
                    <h5 class="text-white-50 mb-2">Nombre total de places</h5>
                    <h2 class="value">{{ allSpots.length }}</h2>
                </div>
            </div>

            <div class="bg-dark mt-3 p-3 rounded-3 d-flex flex-column align-items-center">
                <h3>Vue de: {{ currentParking.name }}</h3>
                <div class="d-flex flex-wrap justify-content-between">
                    <div v-for="(spot) in allSpots" :key="spot.id" class="parking-spot text-center"
                            :class="{'free-spot': spot.status === 'libre',
                                    'occupied-spot': spot.status === 'occupée',
                                    'ms-3': spot.spot_number%2 !== 0,
                                    'me-3': spot.spot_number%2 === 0}" @click="spot.status == 'libre' ? bookSpot(spot.id) : releaseSpot(spot.id)">
                        {{ spot.id }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000';


@Options({})
export default class Home extends Vue {
    parkings: any[] = [];
    allSpots: any[] = [];
    freeSpots: any[] = [];
    occupiedSpots: any[] = [];

    currentParking: any = {};

    mounted() {
        this.fetchData();
    }

    

    async fetchData() {
        try {
            console.log('Fetching data...');
            
            const parkingsResponse = await axios.get('/api/parkings/');
            this.parkings = parkingsResponse.data;
            this.currentParking = this.parkings[0];

            const allSpotsResponse = await axios.get('/api/spots/');
            this.allSpots = allSpotsResponse.data;
            
            this.sortSpots();
            this.freeSpots = this.allSpots.filter((spot: any) => spot.status === 'libre');
            this.occupiedSpots = this.allSpots.filter((spot: any) => spot.status === 'occupée');

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    sortSpots() {
        this.allSpots.sort((a: any, b: any) => a.id - b.id);
    }

    async bookFirstSpot() {
        const firstFreeSpot = this.freeSpots[0];
        if (firstFreeSpot) {
            this.bookSpot(firstFreeSpot.id);
        } else {
            console.log('Aucune place libre');
        }
        this.sortSpots();
    }

    async bookSpot(placeId: number) {
        const spot = this.allSpots.find((spot: any) => spot.id === placeId);
        if (spot && spot.status === 'libre') {
            try {
                const response = await axios.post(`/api/spots/${placeId}/book/`);
                // console.log(`Place n°: ${placeId} : reservation réussie`, response.data);
                
                spot.status = 'occupée';
                this.freeSpots = this.freeSpots.filter((s: any) => s.id !== placeId);
                this.occupiedSpots.push(spot);

            } catch (error) {
                console.error(`Place n°: ${placeId} : reservation echouée`, error);
            }
        } else {
            console.log(`Place n°: ${placeId} : déjà occupée`);
        }
    }

    async releaseSpot(placeId: number) {
        const spot = this.allSpots.find((spot: any) => spot.id === placeId);
        if (spot && spot.status === 'occupée') {
            try {
                const response = await axios.post(`/api/spots/${placeId}/release/`);
                // console.log(`Place n°: ${placeId} : sortie réussie`, response.data);
                
                spot.status = 'libre';
                this.occupiedSpots = this.occupiedSpots.filter((s: any) => s.id !== placeId);
                this.freeSpots.push(spot);

            } catch (error) {
                console.error(`Place n°: ${placeId} : sortie echouée`, error);
            }
        } else {
            console.log(`Place n°: ${placeId} : déjà libre`);
        }
    }

    bookAll() {
        this.freeSpots.forEach((spot: any) => this.bookSpot(spot.id));
        this.sortSpots();
    }

    unBookAll() {
        this.occupiedSpots.forEach((spot: any) => this.releaseSpot(spot.id));
        this.sortSpots();
    }
    
    toggleMenuItem(event: Event) {
        this.$el.querySelector('.menu-item.active').classList.remove('active');
        (event.target as HTMLElement).classList.add('active');
    }
}
</script>

<style scoped>
.free-spot {
    background-color: lightgray;
    color: black;
}

.occupied-spot {
    background-color: red;
    color: white;
}

.chart-container {
    margin-top: 20px;
}

.parking-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr); /* 2 places + 1 allée */
    gap: 10px;
}

.parking-spot {
    width: 60px;
    height: 30px;
    margin-top: 1.25%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 5px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
}

.parking-spot:hover {
    background-color: #404040;
    color: white;
}


.menu-item {
    padding: 12px 15px;
    margin: 5px 0;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
    color: #cccccc;
}

.menu-item:hover {
    background-color: #404040;
    color: #ffffff;
}

.menu-item.active {
    background-color: #007acc;
    color: #ffffff;
}

</style>