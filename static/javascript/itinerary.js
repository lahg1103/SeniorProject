
class GoogleMap {
    constructor(placeholderList, photoWidth = 800, apiKey) {
        this.placeholders = placeholderList,
        this.width = photoWidth,
        this.apiKey = apiKey,
        this.init()
    }

    async init() {
        if (!this.apiKey) {
            console.log("no API key found");
        }
        for (const placeholder of this.placeholders) {
            try {
                await this.processPlaceholder(placeholder);
            } catch (err) {
                console.error(err);
            }
        }
    }

    async processPlaceholder(placeholder) {
        const mapPlaceholder = placeholder.querySelector('.map');
        const imgPlaceholder = placeholder.querySelector('.img');
        const location = mapPlaceholder.dataset.location;
        const address = mapPlaceholder.dataset.address;
        const queries = [
            `${location}, ${address}`,
            location,
            address
        ];

        try {
            const placeId = await this.getPlaceId(queries);
        
            mapPlaceholder.querySelector('iframe').src = `https://www.google.com/maps/embed/v1/place?key=${this.apiKey}&q=place_id:${placeId}`;

            const photoUrl = await this.getPhoto(placeId);
            const img = document.createElement('img');
            img.src = photoUrl;
            img.className = 'goog-photo';
            imgPlaceholder.appendChild(img);
        } catch (err) {
            console.warn(`No map/photo found for ${location}, ${address}, ${err}`);

            if(mapPlaceholder) mapPlaceholder.remove();
            if (imgPlaceholder) imgPlaceholder.remove();
        }
        

    }

    async getPlaceId(queries) {
        for (const q of queries) {
            const url = `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(q)}&key=${this.apiKey}`;
            try {
                const result = await fetch(url);
                const data = await result.json();

                if (data.status === 'OK' && data.results.length > 0) {
                return data.results[0].place_id;
                }

            } catch (err) {
                console.warn(`Failed query: "${q}"`, err);
            }
        }
    }

    async getPhoto(placeId) {
        const url = `https://places.googleapis.com/v1/places/${placeId}`;
        const result = await fetch(url, {
            headers: {
                'X-Goog-Api-Key': this.apiKey,
                'X-Goog-FieldMask': 'photos'
            }
        });
        const data = await result.json();
        if (!data.photos || data.photos.length === 0) throw new Error('No photos found'); 
        return `https://places.googleapis.com/v1/${data.photos[0].name}/media?maxWidthPx=${this.width}&key=${this.apiKey}`;
    }
}

document.addEventListener('DOMContentLoaded', ()=>{
    const googlePlaceholder = document.querySelectorAll('.google');

    const googleMap = new GoogleMap(googlePlaceholder, 800, apiKey);

});