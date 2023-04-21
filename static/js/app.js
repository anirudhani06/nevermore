$(document).ready(function () {
  const hamburger = $('.hamburger');
  hamburger.click(() => {
    $('.overlay').toggleClass('active');
    $('.mobile-links').toggleClass('active');
    hamburger.toggleClass('active');
  });

  const dropDown = $('#drop-down');
  dropDown.click(() => {
    console.log('clicked');
    $('.drop-down-links').toggleClass('active');
  });
});
