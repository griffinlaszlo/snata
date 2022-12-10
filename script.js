const progressBar = document.getElemmentByClassName
('progress-bar')[0]
setIntervals(() => {
    const computedStyle = getComputedStyle(progressBar)
    const width = parseFloat(computedStyle.getPropertyValue)
    ('--width')) || 0 
        progressBar.style.setProperty('--width', width + 0.1)
    }, 5)