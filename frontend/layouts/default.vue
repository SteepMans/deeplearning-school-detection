<template>
  <v-app dark>
    <v-container>
      <Upload :dialog.sync="uploadDialog" :required="true" :multiple="true" @filesUploaded="processUpload($event)" />
      <ImagesPredict v-if="images.length > 0" @startUpload="openUpload" :images="images" />
    </v-container>
  </v-app>
</template>

<script>
export default {
  name: 'DefaultLayout',
  
  data () {
    return {
      uploadDialog: true,
      images: []
    }
  },

  methods: {
    openUpload() {
      this.uploadDialog = true;
    },

    async processUpload(files) {
      var formData = new FormData();

      for (var file of files) {
        formData.append('files', file);
      }

      const predicts = await this.$axios.post(`http://${window.location.hostname}:3001/v1/yolov5/uploads`, formData, {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'multipart/form-data'
        }
      });

      for (var [index, file] of files.entries()) {
        var data = {
          image: file,
          url: URL.createObjectURL(file),
          predict: predicts.data[index]
        }

        const promise = await new Promise((resolve, reject) => {
          const img = new Image();
          img.src = data.url;

          img.onload = () => {
            const width  = img.naturalWidth;
            const height = img.naturalHeight; 

            resolve({width, height});
          };

          img.onerror = reject;
        });

        data.naturalSize = promise;

        this.$store.commit('images/push', data);
        this.images.push(data);
      }
    }
  }
}
</script>

<style lang="scss">

</style>