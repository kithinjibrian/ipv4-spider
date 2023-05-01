<template>
    <v-container class="fill-height">
        <v-responsive class="d-flex fill-height">
            <v-row>
                <v-col cols="6">
                    <v-sheet
                    class="mx-auto">
                        <v-card>
                            <v-card-title>
                                General Information
                            </v-card-title>
                        </v-card>
                    </v-sheet>
                </v-col>
                <v-col cols="6">
                    <v-sheet
                    class="ma-2">
                        <v-card>
                            <v-card-title>
                                Open ports
                            </v-card-title>
                            <v-card-text>
                                <v-chip
                                v-for="i in ip"
                                :key="i">
                                    {{ i.port }}
                                </v-chip>
                            </v-card-text>
                        </v-card>
                    </v-sheet>
                    <v-sheet
                    v-for="i in ip"
                    :key="i"
                    class="ma-2">
                        <v-card>
                            <v-card-title>
                                //{{i.port}}/TCP
                            </v-card-title>
                            <v-card-text>
                                <p>name:{{ i.name }}</p>
                                <p>state:{{ i.state }}</p>
                                <p>reason:{{ i.reason }}</p>
                                <p>extrainfo:{{ i.extrainfo }}</p>
                                <p>product:{{ i.product }}</p>
                                <p>conf:{{ i.conf }}</p>
                                <p>cpe:{{ i.cpe }}</p>
                                <p>script:</p>
                                <div class='ml-10' v-if="i.script!==''">
                                    <p
                                    v-for="m in Object.keys(i.script)"
                                    :key="m">
                                        {{m}} : {{ i.script[m] }}
                                    </p>
                                </div>
                            </v-card-text>
                        </v-card>
                    </v-sheet>
                </v-col>
            </v-row>
        </v-responsive>
    </v-container>
</template>

<script setup>
import { useAppStore } from '@/store/app';
import { useRoute } from 'vue-router'

const store = useAppStore()
const route = useRoute()

const ip = store.ip[route.query.ip]
</script>