<template>
  <v-dialog @click:outside="closeDialog" :persistent="requiredUpload" :value="dialog" max-width="450px">
    <v-card
      @drop.prevent="onDrop($event)"
      @dragover.prevent="dragover = true"
      @dragenter.prevent="dragover = true"
      @dragleave.prevent="dragover = false"
      :class="[{ 'grey ': dragover }, 'upload-icon-hover']"
    >
      <v-card-text>
        <v-row class="d-flex flex-column" dense align="center" justify="center">
          <input @change="handleFileUpload" type="file">
            <v-icon :class="[dragover ? 'mb-8 mt-10' : 'mt-5 mb-1']" size="70">
              mdi-cloud-upload
            </v-icon>
          </input>
          <p>
            Drop your file(s) image <b>(png, jpg, jpeg)</b>, or click to select them.
          </p>
        </v-row>
        <v-virtual-scroll
          v-if="uploadedFiles.length > 0"
          :items="uploadedFiles"
          height="150"
          item-height="50"
        >
          <template v-slot:default="{ item }">
            <v-list-item :key="item.name">
              <v-list-item-content>
                <v-list-item-title>
                  {{ item.name }}
                  <span class="ml-3 text--secondary">
                    {{ item.size }} bytes</span
                  >
                </v-list-item-title>
              </v-list-item-content>

              <v-list-item-action>
                <v-btn @click.stop="removeFile(item.name)" icon>
                  <v-icon> mdi-close-circle </v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>

            <v-divider></v-divider>
          </template>
        </v-virtual-scroll>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn icon @click.stop="submit" v-if="this.uploadedFiles.length > 0">
          <v-icon id="upload-button">mdi-upload</v-icon>
        </v-btn>
      </v-card-actions>

      <div class="upload-notification">
        <v-alert
          :type="item.type"
          v-for="(item, index) in notification" 
          :key="index"
          transition="scroll-y-transition"
          :value="item.show"
          width="100%"
        >{{ item.message }}</v-alert>
      </div>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: "Upload",
  props: {
    dialog: {
      type: Boolean,
      required: true
    },
    multiple: {
      type: Boolean,
      default: false
    },
    required: {
      type: Boolean,
      default: false
    }
  },

  data() {
    return {
      requiredUpload: false,
      dragover: false,
      uploadedFiles: [],
      notification: [],
      fileType: ["png", "jpg", "jpeg", "md"]
    };
  },

  created() {
    setInterval(() => {
      for (var item of this.notification) {
        if (new Date() - item.time > 3000) {
          if (item.show) {
            item.show = false;
            break;
          } else {
            this.notification.splice(this.notification.indexOf(item), 1);
          }
        }
      }
    }, 1000);

    this.requiredUpload = this.required;
  },

  methods: {
    handleFileUpload(e) {
      this.addFiles(e.target.files)
    },

    addNotification(message, type = "error") {
      this.notification.push({
        message: message,
        type: type,
        show: true,
        time: new Date()
      });
    },

    closeDialog() {
      if (!this.requiredUpload) {
        this.uploadedFiles = [];
        this.$emit("update:dialog", false);
      }
    },

    removeFile(fileName) {
      const index = this.uploadedFiles.findIndex(
        file => file.name === fileName
      );

      if (index > -1) 
        this.uploadedFiles.splice(index, 1);
    },
    
    addFiles(files) {
      for (var item of files) {
        let fileType = item.name.split(".").pop();
        
        if (this.fileType.indexOf(fileType) != -1) {
          this.uploadedFiles.push(item)
        } else {
          this.addNotification(`${item.name} file type error`);
        }
      }
    },

    onDrop(e) {
      this.dragover = false;
      
      if (this.uploadedFiles.length > 0) 
        this.uploadedFiles = [];

      if (!this.multiple && e.dataTransfer.files.length > 1) {
        this.$store.dispatch("addNotification", {
          message: "Only one file can be uploaded at a time..",
          colour: "error"
        });
      }
      else {
        this.addFiles(e.dataTransfer.files);
      }
    },

    submit() {
      if (!this.uploadedFiles.length > 0) {
        this.$store.dispatch("notification/add", {
          message: "There are no files to upload",
          colour: "error"
        });
      } else {
        this.$emit("filesUploaded", this.uploadedFiles);
        this.requiredUpload = false;
        this.closeDialog();
      }
    }
  }
};
</script>

<style lang="scss">
.upload-icon-hover:hover {
  input {
    cursor: pointer;
  }

  i {
    color: grey;
  }
}

input {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
}

</style>>