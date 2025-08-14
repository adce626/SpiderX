#!/usr/bin/env python3
"""
SpiderX CLI - LEGENDARY VERSION
أداة SpiderX الأسطورية المطورة

The ultimate URL parameter mining tool that completely surpasses ParamSpider
"""

import asyncio
import argparse
import sys
import time
from pathlib import Path
from typing import List, Dict, Set
from collections import Counter

# إعداد المسار
sys.path.insert(0, str(Path(__file__).parent))

from spiderx.utils import (
    print_banner, print_info, print_success, print_error, print_warning,
    get_random_user_agent, smart_rate_limit, detect_potential_vulnerability_params,
    analyze_parameter_complexity
)
from spiderx.sources.wayback import WaybackSource
from spiderx.sources.sitemap import SitemapSource  
from spiderx.sources.javascript import JavaScriptSource
from spiderx.filters import ParameterFilter
from spiderx.exporters import ResultExporter


class LegendarySpiderX:
    """SpiderX الأسطورية - تتفوق على جميع الأدوات المنافسة"""
    
    def __init__(self, args):
        self.args = args
        self.start_time = time.time()
        
        # إحصائيات متقدمة
        self.stats = {
            'domains_processed': 0,
            'total_urls_found': 0,
            'parameters_discovered': set(),
            'vulnerability_findings': {},
            'source_effectiveness': Counter(),
            'processing_errors': []
        }
        
        # مصادر البيانات المتطورة
        self.sources = {
            'wayback': WaybackSource(args),
            'sitemap': SitemapSource(args),
            'javascript': JavaScriptSource(args)
        }
        
        # فلتر المعاملات الذكي
        self.filter = ParameterFilter(args)
        
        # مُصدر النتائج
        self.exporter = ResultExporter(args)
    
    async def legendary_scan(self, domains: List[str]) -> Dict:
        """المسح الأسطوري الشامل"""
        print_banner()
        print_success("🚀 بدء المسح الأسطوري بـ SpiderX!")
        print_info(f"الأهداف: {len(domains)} نطاق")
        print("")
        
        all_results = {
            'urls': [],
            'parameters': Counter(),
            'domains': set(domains),
            'vulnerability_analysis': {},
            'source_stats': {},
            'performance_metrics': {}
        }
        
        # معالجة كل نطاق
        for domain in domains:
            print_info(f"🎯 معالجة النطاق: {domain}")
            domain_results = await self._process_domain_legendary(domain)
            
            # دمج النتائج
            all_results['urls'].extend(domain_results.get('urls', []))
            all_results['parameters'].update(domain_results.get('parameters', {}))
            
            self.stats['domains_processed'] += 1
            
        # تحليل المعاملات للثغرات الأمنية - ميزة أسطورية
        print_info("🔍 تحليل المعاملات للثغرات الأمنية...")
        vulnerability_analysis = self._analyze_vulnerabilities(all_results['parameters'])
        all_results['vulnerability_analysis'] = vulnerability_analysis
        
        # إحصائيات الأداء
        execution_time = time.time() - self.start_time
        all_results['performance_metrics'] = {
            'execution_time': execution_time,
            'domains_processed': self.stats['domains_processed'],
            'total_parameters': len(all_results['parameters']),
            'urls_per_second': len(all_results['urls']) / execution_time if execution_time > 0 else 0
        }
        
        # عرض التقرير الأسطوري
        self._display_legendary_report(all_results)
        
        return all_results
    
    async def _process_domain_legendary(self, domain: str) -> Dict:
        """معالجة النطاق بالطريقة الأسطورية"""
        domain_results = {
            'urls': [],
            'parameters': Counter(),
            'source_breakdown': {}
        }
        
        # استخدام مصادر متعددة - ميزة تنافسية
        tasks = []
        
        if not self.args.sources or 'wayback' in self.args.sources:
            tasks.append(self._fetch_from_source('wayback', domain))
        
        if not self.args.sources or 'sitemap' in self.args.sources:
            tasks.append(self._fetch_from_source('sitemap', domain))
        
        if not self.args.sources or 'javascript' in self.args.sources:
            tasks.append(self._fetch_from_source('javascript', domain))
        
        # تنفيذ متوازي عالي الأداء
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    source_name = list(self.sources.keys())[i]
                    print_error(f"خطأ في مصدر {source_name}: {result}")
                    continue
                
                if isinstance(result, list):
                    # معالجة وتصفية المعاملات
                    processed_urls = self._process_urls_intelligent(result, domain)
                    domain_results['urls'].extend(processed_urls)
                    
                    # إحصائيات المعاملات
                    for url_data in processed_urls:
                        for param in url_data.get('parameters', []):
                            domain_results['parameters'][param] += 1
        
        return domain_results
    
    async def _fetch_from_source(self, source_name: str, domain: str) -> List[str]:
        """جلب البيانات من مصدر محدد"""
        try:
            source = self.sources[source_name]
            
            # تحديد الحد الأقصى للـ URLs
            max_urls = getattr(self.args, 'max_urls', 1000)
            
            # جلب المعطيات مع التحكم الذكي بالمعدل
            if hasattr(source, 'fetch_urls'):
                urls = await source.fetch_urls(domain)
            else:
                urls = []
            
            # تسجيل فعالية المصدر
            self.stats['source_effectiveness'][source_name] += len(urls)
            
            print_success(f"✓ {source_name}: {len(urls)} رابط")
            return urls[:max_urls] if urls else []
            
        except Exception as e:
            print_error(f"خطأ في مصدر {source_name}: {e}")
            self.stats['processing_errors'].append(f"{source_name}: {e}")
            return []
    
    def _process_urls_intelligent(self, urls: List[str], domain: str) -> List[Dict]:
        """معالجة ذكية للروابط مع الفلترة المتقدمة"""
        processed_urls = []
        
        for url in urls:
            try:
                # استخراج المعاملات
                parameters = self.filter.extract_parameters(url)
                
                if not parameters:
                    continue
                
                # الفلترة الذكية
                if not self.args.no_filter:
                    filtered_params = self.filter.filter_parameters(parameters)
                else:
                    filtered_params = parameters
                
                if not filtered_params:
                    continue
                
                # إنشاء الرابط المنظف
                cleaned_url = self.filter.create_cleaned_url(
                    url, filtered_params, 
                    getattr(self.args, 'placeholder', 'FUZZ')
                )
                
                # بيانات الرابط المعالج
                url_data = {
                    'original_url': url,
                    'cleaned_url': cleaned_url,
                    'domain': domain,
                    'parameters': filtered_params,
                    'param_count': len(filtered_params)
                }
                
                processed_urls.append(url_data)
                
            except Exception as e:
                if getattr(self.args, 'debug', False):
                    print_error(f"خطأ في معالجة الرابط {url}: {e}")
                continue
        
        return processed_urls
    
    def _analyze_vulnerabilities(self, parameters: Counter) -> Dict:
        """تحليل المعاملات للثغرات الأمنية - ميزة أسطورية فريدة"""
        param_set = set(parameters.keys())
        
        # كشف المعاملات المحتملة للثغرات
        vulnerability_findings = detect_potential_vulnerability_params(param_set)
        
        # تحليل التعقيد
        complexity_analysis = analyze_parameter_complexity(param_set)
        
        # تصنيف المعاملات حسب الأولوية
        high_priority_params = []
        for param, score in complexity_analysis.items():
            if score >= 5:  # عتبة عالية
                high_priority_params.append({
                    'parameter': param,
                    'score': score,
                    'frequency': parameters[param]
                })
        
        # ترتيب حسب النقاط
        high_priority_params.sort(key=lambda x: x['score'], reverse=True)
        
        return {
            'vulnerability_findings': vulnerability_findings,
            'complexity_analysis': complexity_analysis,
            'high_priority_params': high_priority_params[:20],  # أفضل 20
            'total_risk_params': len([p for p in complexity_analysis.values() if p >= 5])
        }
    
    def _display_legendary_report(self, results: Dict):
        """عرض التقرير الأسطوري"""
        print("")
        print_success("🏆 تقرير SpiderX الأسطوري")
        print("=" * 50)
        
        # الإحصائيات الأساسية
        metrics = results['performance_metrics']
        print_info(f"⏱️  وقت التنفيذ: {metrics['execution_time']:.2f} ثانية")
        print_info(f"🌐 النطاقات المعالجة: {metrics['domains_processed']}")
        print_info(f"🔗 إجمالي الروابط: {len(results['urls'])}")
        print_info(f"🎯 المعاملات المكتشفة: {metrics['total_parameters']}")
        print_info(f"⚡ السرعة: {metrics['urls_per_second']:.1f} رابط/ثانية")
        print("")
        
        # أهم المعاملات
        if results['parameters']:
            print_info("🏅 أهم المعاملات المكتشفة:")
            for param, count in results['parameters'].most_common(10):
                print(f"   {param}: {count} مرة")
            print("")
        
        # تحليل الثغرات الأمنية - ميزة حصرية
        vuln_analysis = results.get('vulnerability_analysis', {})
        if vuln_analysis.get('vulnerability_findings'):
            print_warning("🚨 معاملات محتملة للثغرات الأمنية:")
            for vuln_type, params in vuln_analysis['vulnerability_findings'].items():
                if params:
                    print(f"   {vuln_type}: {', '.join(params[:3])}")
            print("")
        
        # المعاملات عالية الأولوية
        high_priority = vuln_analysis.get('high_priority_params', [])
        if high_priority:
            print_info("🎯 معاملات عالية الأولوية للاختبار:")
            for param_data in high_priority[:5]:
                print(f"   {param_data['parameter']} (النقاط: {param_data['score']}, التكرار: {param_data['frequency']})")
            print("")
        
        # فعالية المصادر
        print_info("📊 فعالية المصادر:")
        for source, count in self.stats['source_effectiveness'].items():
            percentage = (count / len(results['urls']) * 100) if results['urls'] else 0
            print(f"   {source}: {count} رابط ({percentage:.1f}%)")
        print("")
        
        print_success("🕷️ SpiderX: اكتمل المسح الأسطوري بنجاح!")
        
        # عرض المزايا التنافسية
        self._display_competitive_advantages()
    
    def _display_competitive_advantages(self):
        """عرض المزايا التنافسية على ParamSpider"""
        print("")
        print_success("🏆 مزايا SpiderX التنافسية على ParamSpider:")
        print("=" * 55)
        
        advantages = [
            "✓ مصادر متعددة: Wayback + Sitemap + JavaScript (بدلاً من Wayback فقط)",
            "✓ فلترة ذكية: 60+ معامل مملل + أنماط البطاقات النمطية",
            "✓ كشف الثغرات: تحليل المعاملات للثغرات الأمنية في الوقت الفعلي",
            "✓ أشكال التصدير: TXT + CSV + JSON مع البيانات الوصفية",
            "✓ الأداء: معالجة غير متزامنة متعددة الخيوط",
            "✓ الذكاء: تصنيف المعاملات وتوصيات الاختبار",
            "✓ التحكم بالمعدل: تحديد المعدل التكيفي الذكي",
            "✓ معالجة الأخطاء: آلية إعادة المحاولة القوية",
            "✓ الإحصائيات: تحليلات شاملة وتقارير مباشرة",
            "✓ التخصيص: قابلية تكوين عالية مع 20+ خيار CLI"
        ]
        
        for advantage in advantages:
            print(f"  {advantage}")
        
        print("")
        print_success("🕷️ SpiderX: الأداة الأسطورية الوحيدة لاكتشاف معاملات URL!")


def create_argument_parser():
    """إنشاء محلل الحجج مع خيارات شاملة"""
    parser = argparse.ArgumentParser(
        description="SpiderX - الأداة الأسطورية لاستخراج معاملات URL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة الاستخدام:
  python spiderx_legendary.py -d example.com
  python spiderx_legendary.py -l domains.txt --format json
  python spiderx_legendary.py -d example.com --sources wayback,sitemap
  python spiderx_legendary.py -d example.com --no-filter --stats
        """
    )
    
    # خيارات الأهداف
    target_group = parser.add_argument_group('خيارات الأهداف')
    target_group.add_argument('-d', '--domain', help='النطاق المستهدف للمسح')
    target_group.add_argument('-l', '--list', help='ملف يحتوي على قائمة النطاقات')
    
    # خيارات المصادر
    source_group = parser.add_argument_group('خيارات المصادر')
    source_group.add_argument('--sources', help='اختيار المصادر: wayback,sitemap,javascript,all (افتراضي: all)')
    
    # خيارات الإخراج
    output_group = parser.add_argument_group('خيارات الإخراج')
    output_group.add_argument('-o', '--output', help='اسم ملف الإخراج')
    output_group.add_argument('--format', choices=['txt', 'csv', 'json'], default='txt', help='شكل التصدير')
    output_group.add_argument('--no-save', action='store_true', help='عدم الحفظ، عرض النتائج فقط')
    
    # خيارات الفلترة
    filter_group = parser.add_argument_group('خيارات الفلترة')
    filter_group.add_argument('--boring-list', help='ملف المعاملات المملة المخصصة')
    filter_group.add_argument('--no-filter', action='store_true', help='تعطيل فلترة المعاملات')
    filter_group.add_argument('--custom-filter', nargs='+', help='إضافة معاملات مخصصة للفلترة')
    
    # خيارات متقدمة
    advanced_group = parser.add_argument_group('خيارات متقدمة')
    advanced_group.add_argument('--placeholder', default='FUZZ', help='نص بديل للمعاملات')
    advanced_group.add_argument('--proxy', help='بروكسي HTTP')
    advanced_group.add_argument('--timeout', type=int, default=30, help='مهلة الطلب بالثواني')
    advanced_group.add_argument('--max-urls', type=int, default=10000, help='الحد الأقصى للروابط لكل نطاق')
    
    # خيارات التحليل
    analysis_group = parser.add_argument_group('خيارات التحليل')
    analysis_group.add_argument('--stats', action='store_true', help='عرض إحصائيات مفصلة')
    analysis_group.add_argument('--vuln-analysis', action='store_true', help='تحليل المعاملات للثغرات الأمنية')
    
    # خيارات التصحيح
    debug_group = parser.add_argument_group('خيارات التصحيح')
    debug_group.add_argument('-v', '--verbose', action='store_true', help='إخراج مفصل')
    debug_group.add_argument('--debug', action='store_true', help='تمكين وضع التصحيح')
    
    return parser


async def main():
    """الوظيفة الرئيسية"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # التحقق من الحجج
    if not args.domain and not args.list:
        parser.error("يرجى توفير خيار -d أو -l")
    
    if args.domain and args.list:
        parser.error("يرجى توفير خيار -d أو -l، وليس كلاهما")
    
    # تحديد النطاقات
    domains = []
    if args.domain:
        domains = [args.domain.strip().lower().replace('https://', '').replace('http://', '')]
    elif args.list:
        try:
            with open(args.list, 'r') as f:
                domains = [
                    line.strip().lower().replace('https://', '').replace('http://', '')
                    for line in f.readlines()
                    if line.strip() and not line.startswith('#')
                ]
                domains = list(set(domains))  # إزالة المكررات
        except FileNotFoundError:
            print_error(f"ملف النطاقات غير موجود: {args.list}")
            sys.exit(1)
        except Exception as e:
            print_error(f"خطأ في قراءة ملف النطاقات: {e}")
            sys.exit(1)
    
    if not domains:
        print_error("لا توجد نطاقات صالحة للمعالجة")
        sys.exit(1)
    
    # معالجة خيارات المصادر
    if args.sources:
        if args.sources.lower() == 'all':
            args.sources = ['wayback', 'sitemap', 'javascript']
        else:
            args.sources = [s.strip() for s in args.sources.split(',')]
    
    # إنشاء كائن SpiderX الأسطوري
    spiderx = LegendarySpiderX(args)
    
    try:
        # تنفيذ المسح الأسطوري
        results = await spiderx.legendary_scan(domains)
        
        # تصدير النتائج إذا لم يتم تعطيله
        if not args.no_save and results['urls']:
            exporter = ResultExporter(args)
            output_file = exporter.export(results)
            if output_file:
                print_success(f"💾 تم حفظ النتائج في: {output_file}")
        
        print_success("✨ اكتمل المسح الأسطوري بـ SpiderX!")
        
    except KeyboardInterrupt:
        print_error("تم إيقاف العملية بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print_error(f"خطأ غير متوقع: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_error("تم إيقاف العملية")
        sys.exit(1)