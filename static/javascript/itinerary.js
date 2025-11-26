class GoogleMap {
    constructor(placeholders, embedKey) {
        this.placeholders = placeholders;
        this.embedKey = embedKey;
        this.init();
    }

    async init() {
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
        const queries = [`${location}, ${address}`, location, address];

        let placeData = null;
        for (const q of queries) {
            try {
                const res = await fetch(`/api/place?address=${encodeURIComponent(q)}`);
                if (!res.ok) continue;
                placeData = await res.json();
                break;
            } catch (err) {
                console.warn(`Failed query: ${q}`, err);
            }
        }

        if (!placeData) {
            console.warn(`No map/photo found for ${location}, ${address}`);
            mapPlaceholder?.remove();
            imgPlaceholder?.remove();
            return;
        }

        mapPlaceholder.querySelector('iframe').src =
            `https://www.google.com/maps/embed/v1/place?key=${this.embedKey}&q=place_id:${placeData.place_id}`;

        if (placeData.photos.length > 0) {
            let photo = placeData.photos[0];
            const img = document.createElement('img');
            img.src = photo;
            img.className = 'goog-photo';
            imgPlaceholder.appendChild(img);
        } else {
            imgPlaceholder?.remove();
        }
    }
}

let summarize = function(summaries) {
    Object.values(summaries).forEach(s => {
        let summary = s.textContent.split(" ", 12).join(" ") + "...";
        s.textContent = summary;
    });
}

document.addEventListener('DOMContentLoaded', ()=>{
    const googlePlaceholder = document.querySelectorAll('.google');
    const summarylist = document.querySelectorAll('.summary');
    summarize(summarylist);

    const googleMap = new GoogleMap(googlePlaceholder, apiKey);

});