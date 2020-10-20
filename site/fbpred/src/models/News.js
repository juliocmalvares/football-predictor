import { Schema, model } from 'mongoose';

const NewSchema = new Schema({
    id: String,
    time: String,
    date: String,
    title: String,
    author: String,
    text: String,
    url: String,
    ratings: Number,
    avaliations: {
        aval_1: String,
        aval_2: String,
        aval_3: String
    }    
});

export default model('New', NewSchema, 'news');
