
require 'xcodeproj'

path = 'xxx.xcodeproj'  # .xcodeproj的路径
project = Xcodeproj::Project.open(path)
targetName = 'xxx'  # 对应的target的名称
target = ""
isDevelopment = ARGV.first  # 执行脚本时传入的第一个参数
isDeug = 1

# 你要添加的文件夹路径
novelRefPaths = Array.[](
    'xxx/res',
    'xxx/src'
)

if isDevelopment == '0' then
    novelRefPaths = Array.[](
        'xxx/res',
        'xxx/src'
    )
end

puts '这是传入的数值:'
puts isDevelopment
if isDevelopment then
    puts '测试环境'
else 
    puts '正式环境'
end

novelRefPaths.each do |path|
    if !File.directory?(path) then
        puts "添加的文件路径不存在:  " + path
        exit 1
    end
end

project.targets.each do |tar|
    target = tar if tar.name == targetName
end

if target == "" then
    puts "没有对应的target:  " + targetName
    exit 1
end


mainGroup = project.main_group
# mainGroup.groups.each do |group|
#     puts group.name
# end

source = mainGroup.find_subpath('Resources')
source.set_source_tree('SOURCE_ROOT')

removeRefs = Array.new
references = source.files
references.each do |ref|
    removeRefs << ref if ref.name == 'res'
    removeRefs << ref if ref.name == 'src'
end

if removeRefs.size > 0 then
    puts "删除之前存在的资源 !"
    build_phars = target.resources_build_phase
    removeRefs.each do |ref|
        puts "删除的资源名:  " + ref.name
        build_phars.remove_file_reference(ref)
    end
end

removeGroups = Array.new
source.children.each do |group|
    removeGroups << group if group.name == 'res'
    removeGroups << group if group.name == 'src'
end

if removeGroups.size > 0 then
    puts '从项目中移除引用: '
    removeGroups.each do |group|
        puts '删除的引用名: ' + group.name
        group.remove_from_project
    end
end

novelRefs = Array.new
novelRefPaths.each do |ref| 
    puts "添加资源："
    puts "路径:  " + ref
    puts ref
    file_ref = source.new_reference(ref)
    novelRefs << file_ref
end

if novelRefs.size > 0 then
    target.add_resources(novelRefs)
    project.save
end

# 删除.h和.m文件的方法
# target.source_build_phase.remove_file_reference(file_ref)
# target.headers_build_phase.remove_file_refernece(file_ref)

