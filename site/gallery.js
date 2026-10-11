async function loadGallery() {
  const gallery = document.getElementById('gallery');
  try {
    const response = await fetch('catalog.json');
    if (!response.ok) throw new Error('Catalog unavailable');
    const entries = await response.json();
    document.getElementById('count').textContent = `(${entries.length})`;
    gallery.replaceChildren();
    if (entries.length === 0) {
      const empty = document.createElement('div');
      empty.className = 'empty';
      const title = document.createElement('h3');
      title.textContent = 'The first experiment starts here.';
      const text = document.createElement('p');
      text.textContent = 'No model outputs have been added yet. Generate a simulation with the prompt above, then submit the single HTML file to the repository.';
      empty.append(title, text);
      gallery.append(empty);
    }
    for (const entry of entries) {
      const card = document.createElement('article');
      card.className = 'card';
      const title = document.createElement('h3');
      title.textContent = entry.model;
      const detail = document.createElement('p');
      detail.textContent = [entry.run, entry.date].filter(Boolean).join(' · ');
      card.append(title, detail);
      if (entry.notes) {
        const notes = document.createElement('p');
        notes.textContent = entry.notes;
        card.append(notes);
      }
      const links = document.createElement('nav');
      links.setAttribute('aria-label', `${entry.model} ${entry.run}`);
      const open = document.createElement('a');
      open.href = entry.url;
      open.target = '_blank';
      open.rel = 'noopener noreferrer';
      open.textContent = 'Open simulation ↗';
      const download = document.createElement('a');
      download.href = entry.url;
      download.download = '';
      download.textContent = 'Download HTML';
      links.append(open, download);
      card.append(links);
      gallery.append(card);
    }
  } catch (error) {
    gallery.textContent = 'The submission catalog could not be loaded. Please refresh, or browse the files on GitHub.';
  }
}
loadGallery();
