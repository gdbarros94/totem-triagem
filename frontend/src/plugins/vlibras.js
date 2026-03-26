export function applyLibrasLongPress(elementRef, storeCallback) {
  if (!elementRef) return;

  let pressTimer;

  const startInteraction = (e) => {
    // Only register long press on the element 
    pressTimer = setTimeout(() => triggerLibras(e.target), 600); // 600ms long press
  };

  const cancelInteraction = () => {
    if (pressTimer) {
      clearTimeout(pressTimer);
    }
  };

  function triggerLibras(target) {
    if (window.getSelection) {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(target);
      selection.removeAllRanges();
      selection.addRange(range);
      
      if (storeCallback) storeCallback();
      // VLibras intercepts text selection naturally on the page if enabled.
    }
  }

  elementRef.addEventListener('touchstart', startInteraction, { passive: true });
  elementRef.addEventListener('touchend', cancelInteraction);
  elementRef.addEventListener('mousedown', startInteraction);
  elementRef.addEventListener('mouseup', cancelInteraction);
  elementRef.addEventListener('mouseleave', cancelInteraction);
}
