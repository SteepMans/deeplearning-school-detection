<template>
    <div class="predict">
        <v-card>
        <v-toolbar
            flat
            color="primary"
            dark
        >
        <v-toolbar-title>Detected result
            <v-btn
                class="mx-4"
                icon
                @click="startLoad"
            >
            <v-icon size="24px">
              mdi-cloud-upload
            </v-icon>
          </v-btn>

        </v-toolbar-title>
        </v-toolbar>
            <v-tabs v-model="activeTab" vertical>
            <v-tab v-for="(item, index) of scaleImages" :key="index">
                {{ "Image " + index }} 
            </v-tab>

            <v-tab-item v-for="(item, index) in scaleImages" :key="index" :eager="true">
                <v-card flat>
                    <div class="predict__images">
                        <img @load="loadImage(index)" :src="item.url" class="predict__image" ref="predictImage">
                        <div v-for="(predict, predictIndex) in item.predict" :key="predictIndex" class="predict__block" :style="{'border': `3px solid ${getRandomColor()}`, 'top' : `${predict.ymin}%`, 'left': `${predict.xmin}%`, 'height': `${predict.height}%`, 'width': `${predict.width}%`}">
                            <p class="predict__text">{{ predict.name }} <br> {{ predict.confidence.toFixed(3) }}</p> 
                        </div>
                    </div>
                </v-card>
            </v-tab-item>
        </v-tabs>
    </v-card>
    </div>
</template>

<script>
import { cloneDeep } from 'lodash-es'

export default {
    props: ["images"],

    data () {
        return {
            activeTab: 0,
            scaleImages: null,
            currentImageIndex: 0
        }
    },

    methods: {
        startLoad() {
            this.$emit('startUpload');
        },

        confidenceRound(value) {
            return Math.round10(value, -1);
        },

        getRandomColor() {
            var letters = '0123456789ABCDEF';
            var color = '#';

            for (var i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            
            return color;
        },

        loadImage(e) {
            this.rescale(e);
        },

        rescale(index) {
            const clientImageWidth = document.getElementsByClassName("v-window__container")[0].offsetWidth;
            const clientImageHeight = document.getElementsByClassName("v-window__container")[0].offsetHeight;

            for (var item of this.scaleImages) {
                if (item.rescale)
                    continue;

                const defualtImageWidth = item.naturalSize.width;
                const defualtImageHeight = item.naturalSize.height;
    
                var scaleWidth = clientImageWidth * 100.0 / defualtImageWidth / 100;
                var scaleHeight = clientImageHeight * 100.0 / defualtImageHeight / 100;
    
                for (var predict of item.predict) {
                    predict.ymin = predict.ymin * scaleHeight * 100 / clientImageHeight;
                    predict.ymax = predict.ymax * scaleHeight * 100 / clientImageHeight;

                    predict.xmin = predict.xmin * scaleWidth * 100 / clientImageWidth;
                    predict.xmax = predict.xmax * scaleWidth * 100 / clientImageWidth;

                    predict.width = predict.xmax - predict.xmin;
                    predict.height = predict.ymax - predict.ymin;
                }

                item.rescale = true;
            }
        },

        rescaleAll() {
            this.scaleImages.map((x, index) => this.rescale(index))
        },
    },

    watch: {
        images(newObject, oldObject) {
            this.scaleImages = this.scaleImages.concat(cloneDeep(this.images.slice(-1)))
        }
    },

    mounted() {
        this.scaleImages = cloneDeep(this.images);
    }
}
</script>

<style lang="scss">
.predict {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;

    &__images {
        position: relative;
        width: min-content;
    }

    img {
        overflow: auto;
        max-width: 30vw;
        max-height: 70vh;
    }

    &__text {
        white-space: nowrap;
        font-weight: 500;
        font-size: 90%;
        line-height: 1.5vh;
        text-transform: uppercase;
        text-shadow: 1px 1px 1px #000;
    }

    &__block:hover {
        opacity: 1.0;
        transition-duration: 0.3s;
    }

    &__block {
        opacity: 0.3;
        transition-duration: 0.3s;
        position: absolute;
    }
}
</style>