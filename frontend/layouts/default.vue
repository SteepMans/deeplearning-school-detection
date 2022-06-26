<template>
  <v-app dark>
    <v-container>
      <Upload :dialog.sync="uploadDialog" :multiple="true" @filesUploaded="processUpload($event)" />
      <ImagesPredict v-if="images.length > 0" :images="images" />
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
    async processUpload(files) {
      var formData = new FormData();

      for (var file of files) {
        formData.append('files', file);
      }
      
      const predicts = await this.$axios.post('http://127.0.0.1:8000/v1/yolov5/uploads', formData, {
        headers: {
          'accept': 'application/json',
          'Content-Type': 'multipart/form-data'
        }
      });

      for (var [index, file] of files.entries()) {
        var data = {
          image: file,
          url: URL.createObjectURL(files[0]),
          predict: predicts.data[index]
        }

        this.$store.commit('images/push', data);
        this.images.push(data);
      }
    }
  }
}
</script>

<style lang="scss">

</style>