const mongoose = require('mongoose');

const UserSchema = new mongoose.Schema(
    {
    userID: Number,
    username: String,
    email:String,
    password: String,
},
{
    timestamps: true,
}
);

const User = mongoose.model('User', UserSchema);

module.exports = User;