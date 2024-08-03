from django.shortcuts import render
from .forms import URLForm
from .scraper import scrape_product, initialize_webdriver

def scrape_view(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            wd = initialize_webdriver()
            if not wd:
                return render(request, 'product_scraper/result.html', {'error': 'Failed to initialize WebDriver'})

            try:
                product_data = scrape_product(wd, url)
                if not product_data:
                    return render(request, 'product_scraper/result.html', {'error': 'Failed to scrape product data'})
                
                return render(request, 'product_scraper/result.html', {'products': product_data})
            except Exception as e:
                return render(request, 'product_scraper/result.html', {'error': f'Error during scraping: {e}'})
    else:
        form = URLForm()

    return render(request, 'product_scraper/scrape_form.html', {'form': form})
